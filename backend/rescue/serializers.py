from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Max
from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import RescueCase, RescueStageRecord, RescueStatusLog


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


class RescueStatusLogSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)

    class Meta:
        model = RescueStatusLog
        fields = '__all__'


class RescueCaseSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    helpers = UserSerializer(many=True, read_only=True)
    status_logs = RescueStatusLogSerializer(many=True, read_only=True)
    discover_latitude = CoordinateField()
    discover_longitude = CoordinateField()

    class Meta:
        model = RescueCase
        fields = '__all__'
        read_only_fields = ['rescue_no', 'reporter', 'helpers', 'help_date', 'created_at', 'updated_at']

    def validate_discover_address(self, value):
        text = (value or '').strip()
        if not text:
            raise serializers.ValidationError('\u8bf7\u586b\u5199\u53d1\u73b0\u5730\u70b9\u6216\u9644\u8fd1\u5730\u6807\u3002')
        return text

    def validate_nickname(self, value):
        text = (value or '').strip()
        if not text:
            raise serializers.ValidationError('\u8bf7\u586b\u5199\u60a8\u7684\u6635\u79f0\u3002')
        return text

    def validate_contact(self, value):
        text = (value or '').strip()
        if not text:
            raise serializers.ValidationError('\u8bf7\u586b\u5199\u60a8\u7684\u8054\u7cfb\u65b9\u5f0f\u3002')
        if len(text) < 5:
            raise serializers.ValidationError('\u8054\u7cfb\u65b9\u5f0f\u683c\u5f0f\u4e0d\u6b63\u786e\uff0c\u8bf7\u586b\u5199\u624b\u673a\u53f7\u6216\u5fae\u4fe1\u53f7\u3002')
        return text


class RescueStageRecordSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)

    class Meta:
        model = RescueStageRecord
        fields = ['id', 'rescue_case', 'content', 'operator', 'created_at']
        read_only_fields = ['rescue_case', 'operator', 'created_at']


def generate_rescue_no():
    today = datetime.now().strftime('%Y%m%d')
    prefix = f'RES{today}'
    last = RescueCase.objects.filter(rescue_no__startswith=prefix).aggregate(Max('rescue_no'))['rescue_no__max']
    # 格式 RES20260614001（年月日 + 3位流水号）
    seq = int(last[-3:]) + 1 if last else 1
    return f'{prefix}{seq:03d}'
