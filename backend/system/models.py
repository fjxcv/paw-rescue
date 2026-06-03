from django.contrib.auth.models import User
from django.db import models


class OperationLog(models.Model):
    operator = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='operation_logs')
    module = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    target_type = models.CharField(max_length=50, blank=True, null=True)
    target_id = models.BigIntegerField(blank=True, null=True)
    content = models.TextField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'operation_log'
        ordering = ['-created_at']


class ContentModeration(models.Model):
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('hide', 'Hide'),
        ('delete', 'Delete'),
    ]

    content_type = models.CharField(max_length=30)
    content_id = models.BigIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='moderation_actions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_moderation'
        ordering = ['-created_at']


class PlatformConfig(models.Model):
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.TextField()
    description = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'platform_config'


class AiInvocationLog(models.Model):
    FEATURE_CHOICES = [
        ('breed_detect', 'Breed Detect'),
        ('adopt_copy', 'Adopt Copy'),
        ('qa_assistant', 'QA Assistant'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_invocations')
    feature_type = models.CharField(max_length=30, choices=FEATURE_CHOICES)
    request_meta = models.TextField(blank=True, null=True)
    result_meta = models.TextField(blank=True, null=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_invocation_log'
        ordering = ['-created_at']
