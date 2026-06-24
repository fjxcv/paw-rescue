from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import AiInvocationLog, ContentModeration, OperationLog, PlatformConfig


class OperationLogSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)

    class Meta:
        model = OperationLog
        fields = '__all__'


class ContentModerationSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)

    class Meta:
        model = ContentModeration
        fields = '__all__'
        read_only_fields = ['operator', 'created_at']

    def validate(self, attrs):
        action = attrs.get('action') or getattr(self.instance, 'action', None)
        reason = (attrs.get('reason') or '').strip()
        if action in ('hide', 'delete', 'ban') and not reason:
            raise serializers.ValidationError({'reason': '\u5904\u7f6e\u539f\u56e0\u4e0d\u80fd\u4e3a\u7a7a'})
        if action == 'ban' and attrs.get('content_type') != 'user':
            raise serializers.ValidationError({'content_type': 'ban action requires content_type=user'})
        return attrs


class PlatformConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformConfig
        fields = '__all__'


class AiInvocationLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AiInvocationLog
        fields = '__all__'
        read_only_fields = ['user', 'success', 'created_at']
