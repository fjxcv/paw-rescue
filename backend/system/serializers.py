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
