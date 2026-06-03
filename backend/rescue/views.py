from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsAdminRole
from common.utils import get_client_ip, write_operation_log
from .models import RescueCase, RescueStatusLog
from .serializers import RescueCaseSerializer, generate_rescue_no


class RescueCaseViewSet(viewsets.ModelViewSet):
    queryset = RescueCase.objects.select_related('reporter').prefetch_related('status_logs').all()
    serializer_class = RescueCaseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        case = serializer.save(reporter=self.request.user, rescue_no=generate_rescue_no())
        RescueStatusLog.objects.create(
            rescue_case=case,
            from_status=None,
            to_status=case.current_status,
            operator=self.request.user,
            remark='Case created',
        )

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        case = self.get_object()
        new_status = request.data.get('current_status')
        valid = dict(RescueCase.STATUS_CHOICES)
        if new_status not in valid:
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        old_status = case.current_status
        case.current_status = new_status
        case.save(update_fields=['current_status', 'updated_at'])
        RescueStatusLog.objects.create(
            rescue_case=case,
            from_status=old_status,
            to_status=new_status,
            operator=request.user,
            remark=request.data.get('remark', ''),
        )
        write_operation_log(
            request.user, 'rescue', 'status_change',
            f'Rescue {case.rescue_no}: {old_status} -> {new_status}',
            'rescue_case', case.id, get_client_ip(request),
        )
        return Response(self.get_serializer(case).data)
