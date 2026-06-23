from decimal import Decimal, ROUND_HALF_UP

from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import LostFoundPost


def _round_coordinate(value):
    if value is None or value == '':
        return None
    return Decimal(str(value)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)


class CoordinateField(serializers.DecimalField):
    def __init__(self, **kwargs):
        kwargs.setdefault('max_digits', 9)
        kwargs.setdefault('decimal_places', 6)
        kwargs.setdefault('required', False)
        kwargs.setdefault('allow_null', True)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data in (None, ''):
            return None
        return super().to_internal_value(_round_coordinate(data))


class LostFoundPostSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    latitude = CoordinateField()
    longitude = CoordinateField()
    contact_phone_display = serializers.SerializerMethodField()

    class Meta:
        model = LostFoundPost
        fields = '__all__'
        read_only_fields = ['publisher', 'created_at', 'updated_at', 'contact_phone_display']

    def get_contact_phone_display(self, obj):
        request = self.context.get('request')
        phone = obj.contact_phone
        if not phone:
            return None
        if request and request.user.is_authenticated:
            if request.user == obj.publisher:
                return phone
            if getattr(request.user.profile, 'role', None) == 'admin':
                return phone
        phone_str = str(phone).strip()
        if len(phone_str) >= 7:
            return phone_str[:3] + '****' + phone_str[-4:]
        return phone_str[:3] + '****'

    def validate_photo_urls(self, value):
        if not value or not isinstance(value, list) or len(value) < 1:
            raise serializers.ValidationError('\u8bf7\u81f3\u5c11\u4e0a\u4f20 1 \u5f20\u5ba0\u7269\u7167\u7247')
        return value

    def validate_address_text(self, value):
        text = (value or '').strip()
        if not text:
            return ''
        return text
