from django.contrib.auth.models import User
from django.db import models


class RescueCase(models.Model):
    STATUS_CHOICES = [
        ('pending_rescue', 'Pending Rescue'),
        ('in_medical', 'In Medical'),
        ('recovering', 'Recovering'),
        ('awaiting_adoption', 'Awaiting Adoption'),
        ('rescued', 'Rescued'),
        ('abandoned', 'Abandoned'),
    ]

    SIZE_CHOICES = [
        ('small', '小型'),
        ('medium', '中型'),
        ('large', '大型'),
    ]

    HEALTH_CHOICES = [
        ('healthy', '健康'),
        ('minor_injury', '轻微伤病'),
        ('severe_injury', '严重伤病'),
    ]

    rescue_no = models.CharField(max_length=32, unique=True)
    reporter = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rescue_cases')
    # 响应救助的用户（可多个）
    helpers = models.ManyToManyField(User, related_name='helped_cases', blank=True)
    # 救助行动开始的日期（首次被响应时记录）
    help_date = models.DateTimeField(null=True, blank=True)
    # 上报人填写信息（允许代他人上报，不使用 profile 自动填充）
    nickname = models.CharField(max_length=50, default='', blank=True)
    contact = models.CharField(max_length=100, default='', blank=True)
    discover_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    discover_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    discover_address = models.CharField(max_length=255)
    size_category = models.CharField(max_length=20, choices=SIZE_CHOICES, default='', blank=True)
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='', blank=True)
    is_injured = models.BooleanField(default=False)
    afraid_of_people = models.BooleanField(default=False)
    appearance = models.TextField(blank=True, null=True)
    health_note = models.TextField(blank=True, null=True)
    photo_urls = models.JSONField(default=list, blank=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_rescue')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rescue_case'
        ordering = ['-created_at']


class RescueStatusLog(models.Model):
    rescue_case = models.ForeignKey(RescueCase, on_delete=models.CASCADE, related_name='status_logs')
    from_status = models.CharField(max_length=20, blank=True, null=True)
    to_status = models.CharField(max_length=20)
    operator = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rescue_status_operations')
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rescue_status_log'
        ordering = ['created_at']


class RescueStageRecord(models.Model):
    """救助各阶段的详细记录，可多次填写"""
    rescue_case = models.ForeignKey(RescueCase, on_delete=models.CASCADE, related_name='stage_records')
    content = models.TextField()
    operator = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rescue_stage_records')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rescue_stage_record'
        ordering = ['-created_at']
