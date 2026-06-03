from rest_framework import permissions, viewsets

from common.permissions import IsAdminRole
from .models import PortalCarousel
from .serializers import PortalCarouselSerializer


class PortalCarouselViewSet(viewsets.ModelViewSet):
    queryset = PortalCarousel.objects.all()
    serializer_class = PortalCarouselSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list' and not (self.request.user.is_authenticated and getattr(self.request.user.profile, 'role', None) == 'admin'):
            qs = qs.filter(status=1)
        return qs
