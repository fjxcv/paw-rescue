from django.contrib.auth.models import User
from django.db import models


class CmsCategory(models.Model):
    STATUS_CHOICES = [(0, 'Disabled'), (1, 'Enabled')]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cms_category'
        ordering = ['sort_order', 'id']


class CmsArticle(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ('science', 'Science'),
        ('announcement', 'Announcement'),
        ('law', 'Law'),
        ('rescue_case', 'Rescue Case'),
    ]
    STATUS_CHOICES = [(0, 'Draft'), (1, 'Published'), (2, 'Offline')]

    category = models.ForeignKey(
        CmsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles'
    )
    author = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='cms_articles')
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField()
    cover_url = models.CharField(max_length=500, blank=True, null=True)
    view_count = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    sort_weight = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_article'
        ordering = ['-is_pinned', '-sort_weight', '-published_at', '-created_at']


class ArticleFavorite(models.Model):
    article = models.ForeignKey(CmsArticle, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_favorite'
        unique_together = [('article', 'user')]
