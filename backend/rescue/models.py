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

    rescue_no = models.CharField(max_length=32, unique=True)
    reporter = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rescue_cases')
    discover_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    discover_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    discover_address = models.CharField(max_length=255)
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
