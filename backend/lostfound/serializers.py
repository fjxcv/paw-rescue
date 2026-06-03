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

    class Meta:
        model = LostFoundPost
        fields = '__all__'
        read_only_fields = ['publisher', 'created_at', 'updated_at']

    def validate_address_text(self, value):
        text = (value or '').strip()
        if not text:
            raise serializers.ValidationError(
                '\u8bf7\u586b\u5199\u4e8b\u53d1\u5730\u70b9\u6216\u9644\u8fd1\u5730\u6807\u3002'
            )
        return text
