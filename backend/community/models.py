from django.contrib.auth.models import User
from django.db import models


class CommunityPost(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('rescue_share', 'Rescue Share'),
        ('help_request', 'Help Request'),
        ('pet_experience', 'Pet Experience'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_urls = models.JSONField(default=list, blank=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'community_post'
        ordering = ['-created_at']


class CommunityComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_replies'
    )
    root = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='thread_replies'
    )
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'community_comment'
        ordering = ['created_at']


class PostLike(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_like'
        unique_together = [('post', 'user')]


class PostFavorite(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_favorite'
        unique_together = [('post', 'user')]


class CommentLike(models.Model):
    comment = models.ForeignKey(CommunityComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_like'
        unique_together = [('comment', 'user')]
