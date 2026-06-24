from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdminRole
from .models import PortalCarousel
from .serializers import PortalCarouselSerializer


class PortalCarouselViewSet(viewsets.ModelViewSet):
    """\u9996\u9875\u8f6e\u64ad\u56fe\u7ba1\u7406"""
    queryset = PortalCarousel.objects.all()
    serializer_class = PortalCarouselSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_authenticators(self):
        if getattr(self, 'action', None) in ['list', 'retrieve']:
            return []
        return super().get_authenticators()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list' and not (
            self.request.user.is_authenticated
            and getattr(getattr(self.request.user, 'profile', None), 'role', None) == 'admin'
        ):
            qs = qs.filter(status=1)
        return qs


class PortalStatsView(APIView):
    """\u9996\u9875\u6838\u5fc3\u6570\u636e\u7edf\u8ba1"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

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
    """\u9996\u9875\u6700\u65b0\u52a8\u6001\u805a\u5408"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

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
            'urgent_lost': LostFoundPostSerializer(urgent_lost, many=True, context=ctx).data,
            'adoptable_pets': PetProfileSerializer(adoptable_pets, many=True, context=ctx).data,
        })
