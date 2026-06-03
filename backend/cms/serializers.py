from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import ArticleFavorite, CmsArticle, CmsCategory


class CmsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsCategory
        fields = '__all__'


class CmsArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = CmsArticle
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ArticleFavorite.objects.filter(article=obj, user=request.user).exists()
        return False


class ArticleFavoriteItemSerializer(serializers.ModelSerializer):
    article = CmsArticleSerializer(read_only=True)

    class Meta:
        model = ArticleFavorite
        fields = ['id', 'created_at', 'article']
