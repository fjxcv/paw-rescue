from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdminRole
from .models import ArticleFavorite, CmsArticle, CmsCategory
from .serializers import (
    ArticleFavoriteItemSerializer,
    CmsArticleSerializer,
    CmsCategorySerializer,
)


class CmsCategoryViewSet(viewsets.ModelViewSet):
    queryset = CmsCategory.objects.all()
    serializer_class = CmsCategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]


class CmsArticleViewSet(viewsets.ModelViewSet):
    queryset = CmsArticle.objects.select_related('category', 'author').all()
    serializer_class = CmsArticleSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'favorite':
            return [permissions.IsAuthenticated()]
        return [IsAdminRole()]

    def get_queryset(self):
        qs = super().get_queryset()
        article_type = self.request.query_params.get('type')
        category_id = self.request.query_params.get('category')
        if article_type:
            qs = qs.filter(article_type=article_type)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if self.action in ['list', 'retrieve'] and not (self.request.user.is_authenticated and getattr(self.request.user.profile, 'role', None) == 'admin'):
            qs = qs.filter(status=1)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 1:
            CmsArticle.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
            instance.refresh_from_db()
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        article = serializer.save()
        if article.status == 1 and not article.published_at:
            article.published_at = timezone.now()
            article.save(update_fields=['published_at'])

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk=None):
        article = self.get_object()
        if article.status != 1:
            return Response(
                {'detail': '\u4ec5\u53ef\u6536\u85cf\u5df2\u53d1\u5e03\u7684\u6587\u7ae0'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == 'POST':
            ArticleFavorite.objects.get_or_create(article=article, user=request.user)
            return Response({'detail': 'Favorited'})
        ArticleFavorite.objects.filter(article=article, user=request.user).delete()
        return Response({'detail': 'Favorite removed'})


class MyArticleFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = (
            ArticleFavorite.objects.filter(user=request.user, article__status=1)
            .select_related('article', 'article__category', 'article__author')
            .order_by('-created_at')
        )
        serializer = ArticleFavoriteItemSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
