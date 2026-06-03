from django.utils import timezone
from rest_framework import serializers

from accounts.serializers import UserSerializer
from pets.models import AdoptApplication, AdoptAttachment, AdoptOfflineVerify, AdoptQuestionnaire, PetProfile


class PetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetProfile
        fields = '__all__'


class AdoptApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    pet = PetProfileSerializer(read_only=True)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=PetProfile.objects.all(), source='pet', write_only=True
    )

    class Meta:
        model = AdoptApplication
        fields = [
            'id', 'applicant', 'pet', 'pet_id', 'online_status', 'audit_opinion',
            'auditor', 'audited_at', 'message', 'created_at', 'updated_at',
        ]
        read_only_fields = ['applicant', 'auditor', 'audited_at', 'created_at', 'updated_at']

    def validate(self, attrs):
        pet = attrs.get('pet') or getattr(self.instance, 'pet', None)
        applicant = self.context['request'].user
        if pet and AdoptApplication.objects.filter(
            applicant=applicant,
            pet=pet,
            online_status__in=['pending', 'approved'],
        ).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError('Duplicate active application for this pet')
        return attrs


class AdoptQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptQuestionnaire
        fields = ['id', 'application', 'answers_json', 'submitted_at']
        read_only_fields = ['application', 'submitted_at']


class AdoptAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptAttachment
        fields = ['id', 'application', 'file_type', 'file_url', 'file_size', 'uploaded_at']
        read_only_fields = ['application', 'uploaded_at']

    def validate_file_size(self, value):
        if value <= 0:
            raise serializers.ValidationError('File size must be greater than 0')
        return value


class AdoptOfflineVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptOfflineVerify
        fields = ['id', 'application', 'verify_status', 'verify_note', 'verifier', 'verified_at']
        read_only_fields = ['application', 'verifier', 'verified_at']


class AdoptApplicationAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptApplication
        fields = ['online_status', 'audit_opinion']

    def update(self, instance, validated_data):
        instance.online_status = validated_data.get('online_status', instance.online_status)
        instance.audit_opinion = validated_data.get('audit_opinion', instance.audit_opinion)
        instance.auditor = self.context['request'].user
        instance.audited_at = timezone.now()
        instance.save()
        if instance.online_status == 'approved':
            instance.pet.adoption_status = 'pending'
            instance.pet.save(update_fields=['adoption_status', 'updated_at'])
        elif instance.online_status == 'rejected':
            if not AdoptApplication.objects.filter(pet=instance.pet, online_status__in=['pending', 'approved']).exclude(pk=instance.pk).exists():
                instance.pet.adoption_status = 'available'
                instance.pet.save(update_fields=['adoption_status', 'updated_at'])
        return instance
