from django.contrib.auth.models import User
from django.db import models


class LostFoundPost(models.Model):
    """报失/寻主记录"""
    POST_TYPE_CHOICES = [('lost', 'Lost'), ('found', 'Found')]
    STATUS_CHOICES = [
        ('searching', 'Searching'),
        ('found', 'Found'),
        ('cancelled', 'Cancelled'),
    ]

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_found_posts')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    pet_species = models.CharField(max_length=50)
    features = models.TextField()
    photo_urls = models.JSONField(default=list, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address_text = models.CharField(max_length=255)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='searching')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lost_found_post'
        ordering = ['-created_at']
