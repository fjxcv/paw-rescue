from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsAdminRole
from common.utils import get_client_ip, write_operation_log
from .models import AdoptApplication, AdoptAttachment, AdoptOfflineVerify, AdoptQuestionnaire, PetProfile
from .serializers import (
    AdoptApplicationAuditSerializer,
    AdoptApplicationSerializer,
    AdoptAttachmentSerializer,
    AdoptOfflineVerifySerializer,
    AdoptQuestionnaireSerializer,
    PetProfileSerializer,
)


class PetProfileViewSet(viewsets.ModelViewSet):
    queryset = PetProfile.objects.all()
    serializer_class = PetProfileSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_queryset(self):
        qs = super().get_queryset()
        species = self.request.query_params.get('species')
        adoption_status = self.request.query_params.get('adoption_status')
        is_public = self.request.query_params.get('is_public')
        if species:
            qs = qs.filter(species=species)
        if adoption_status:
            qs = qs.filter(adoption_status=adoption_status)
        if is_public is not None and self.action in ['list', 'retrieve']:
            if not (self.request.user.is_authenticated and getattr(self.request.user.profile, 'role', None) == 'admin'):
                qs = qs.filter(is_public=True)
        elif is_public is not None:
            qs = qs.filter(is_public=is_public.lower() == 'true')
        return qs


class AdoptApplicationViewSet(viewsets.ModelViewSet):
    queryset = AdoptApplication.objects.select_related('applicant', 'pet', 'auditor').all()
    serializer_class = AdoptApplicationSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action in ['create', 'my', 'questionnaire', 'attachments']:
            return [permissions.IsAuthenticated()]
        return [IsAdminRole()]

    def get_queryset(self):
        if self.action == 'my':
            return self.queryset.filter(applicant=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        app = serializer.save(applicant=self.request.user)
        app.pet.adoption_status = 'pending'
        app.pet.save(update_fields=['adoption_status', 'updated_at'])

    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        qs = self.get_queryset()
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=True, methods=['post'], url_path='questionnaire')
    def questionnaire(self, request, pk=None):
        app = self.get_object()
        if app.applicant != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        if hasattr(app, 'questionnaire'):
            return Response({'detail': 'Questionnaire already submitted'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AdoptQuestionnaireSerializer(data={
            'application': app.id,
            'answers_json': request.data.get('answers_json', {}),
        })
        serializer.is_valid(raise_exception=True)
        AdoptQuestionnaire.objects.create(application=app, answers_json=serializer.validated_data['answers_json'])
        return Response({'detail': 'Questionnaire submitted'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='attachments')
    def attachments(self, request, pk=None):
        app = self.get_object()
        if app.applicant != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        serializer = AdoptAttachmentSerializer(data={
            'application': app.id,
            'file_type': request.data.get('file_type', 'other'),
            'file_url': request.data.get('file_url'),
            'file_size': request.data.get('file_size', 1),
        })
        serializer.is_valid(raise_exception=True)
        attachment = AdoptAttachment.objects.create(
            application=app,
            file_type=serializer.validated_data['file_type'],
            file_url=serializer.validated_data['file_url'],
            file_size=serializer.validated_data['file_size'],
        )
        return Response(AdoptAttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)


class AdminAdoptApplicationViewSet(viewsets.GenericViewSet):
    queryset = AdoptApplication.objects.all()
    serializer_class = AdoptApplicationAuditSerializer
    permission_classes = [IsAdminRole]

    def update(self, request, pk=None):
        app = self.get_object()
        serializer = self.get_serializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        write_operation_log(
            request.user, 'adopt', 'audit',
            f'Adopt application audit #{app.id}: {app.online_status}',
            'adopt_application', app.id, get_client_ip(request),
        )
        return Response(AdoptApplicationSerializer(app).data)


class AdminOfflineVerifyViewSet(viewsets.GenericViewSet):
    queryset = AdoptOfflineVerify.objects.select_related('application').all()
    serializer_class = AdoptOfflineVerifySerializer
    permission_classes = [IsAdminRole]

    def update(self, request, pk=None):
        verify = self.get_object()
        verify.verify_status = request.data.get('verify_status', verify.verify_status)
        verify.verify_note = request.data.get('verify_note', verify.verify_note)
        verify.verifier = request.user
        verify.verified_at = timezone.now()
        verify.save()
        if verify.verify_status == 'passed':
            verify.application.online_status = 'approved'
            verify.application.pet.adoption_status = 'adopted'
        elif verify.verify_status == 'failed':
            verify.application.online_status = 'rejected'
            verify.application.pet.adoption_status = 'available'
        verify.application.save()
        verify.application.pet.save()
        return Response(AdoptOfflineVerifySerializer(verify).data)

    def create_for_application(self, request, application_id=None):
        app = AdoptApplication.objects.get(pk=application_id)
        verify, _ = AdoptOfflineVerify.objects.get_or_create(application=app)
        return Response(AdoptOfflineVerifySerializer(verify).data)
