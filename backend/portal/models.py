from django.db import models


class PortalCarousel(models.Model):
    STATUS_CHOICES = [(0, 'Offline'), (1, 'Online')]

    title = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=500)
    link_url = models.CharField(max_length=500, blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_carousel'
        ordering = ['sort_order', 'id']
