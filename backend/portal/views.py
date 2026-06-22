from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdminRole
from .models import PortalCarousel
from .serializers import PortalCarouselSerializer


class PortalCarouselViewSet(viewsets.ModelViewSet):
    """轮播图管理"""
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


class PortalStatsView(APIView):
    """首页核心数据统计"""
    permission_classes = [permissions.AllowAny()]

    def get(self, request):
        from django.utils import timezone
        from rescue.models import RescueCase
        from pets.models import PetProfile
        from lostfound.models import LostFoundPost

        today = timezone.now().date()
        return Response({
            'total_rescued': RescueCase.objects.filter(current_status='rescued').count(),
            'total_adopted': PetProfile.objects.filter(adoption_status='adopted').count(),
            'searching_count': LostFoundPost.objects.filter(status='searching').count(),
            'today_reported': RescueCase.objects.filter(created_at__date=today).count(),
        })


class PortalDashboardView(APIView):
    """首页最新动态聚合"""
    permission_classes = [permissions.AllowAny()]

    def get(self, request):
        from cms.models import CmsArticle
        from cms.serializers import CmsArticleSerializer
        from lostfound.models import LostFoundPost
        from lostfound.serializers import LostFoundPostSerializer
        from pets.models import PetProfile
        from pets.serializers import PetProfileSerializer

        announcements = CmsArticle.objects.filter(
            article_type='announcement', status=1
        ).order_by('-is_pinned', '-published_at')[:3]

        science_articles = CmsArticle.objects.filter(
            article_type='science', status=1
        ).order_by('-published_at')[:3]

        urgent_lost = LostFoundPost.objects.filter(
            status='searching'
        ).order_by('-created_at')[:3]

        adoptable_pets = PetProfile.objects.filter(
            adoption_status='available', is_public=True
        ).order_by('-created_at')[:4]

        ctx = {'request': request}
        return Response({
            'announcements': CmsArticleSerializer(announcements, many=True, context=ctx).data,
            'science_articles': CmsArticleSerializer(science_articles, many=True, context=ctx).data,
            'urgent_lost': LostFoundPostSerializer(urgent_lost, many=True).data,
            'adoptable_pets': PetProfileSerializer(adoptable_pets, many=True).data,
        })
