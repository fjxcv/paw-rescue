from rest_framework import serializers
from .models import PortalCarousel


class PortalCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalCarousel
        fields = '__all__'
