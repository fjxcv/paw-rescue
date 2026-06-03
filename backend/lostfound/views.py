from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from common.permissions import IsAdminRole
from .models import LostFoundPost
from .serializers import LostFoundPostSerializer


class LostFoundPostViewSet(viewsets.ModelViewSet):
    queryset = LostFoundPost.objects.select_related('publisher').all()
    serializer_class = LostFoundPostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        post_type = self.request.query_params.get('post_type')
        status_val = self.request.query_params.get('status')
        if post_type:
            qs = qs.filter(post_type=post_type)
        if status_val:
            qs = qs.filter(status=status_val)
        search_q = (self.request.query_params.get('q') or self.request.query_params.get('search') or '').strip()
        if search_q:
            qs = qs.filter(
                Q(pet_species__icontains=search_q)
                | Q(features__icontains=search_q)
                | Q(address_text__icontains=search_q)
            )
        species_kw = (self.request.query_params.get('species_keyword') or '').strip()
        if species_kw:
            qs = qs.filter(pet_species__icontains=species_kw)
        return qs

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.publisher != self.request.user and getattr(self.request.user.profile, 'role', None) != 'admin':
            raise PermissionDenied('Not allowed to update this post')
        serializer.save()
