from django.contrib.auth.models import User
from django.db import models

from rescue.models import RescueCase


class PetProfile(models.Model):
    ADOPTION_STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted'),
    ]

    rescue_case = models.ForeignKey(
        RescueCase, on_delete=models.SET_NULL, null=True, blank=True, related_name='pets'
    )
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age_months = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    health_status = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    adoption_status = models.CharField(max_length=20, choices=ADOPTION_STATUS_CHOICES, default='available')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet_profile'
        ordering = ['-created_at']


class AdoptApplication(models.Model):
    ONLINE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('need_material', 'Need Material'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adopt_applications')
    pet = models.ForeignKey(PetProfile, on_delete=models.RESTRICT, related_name='applications')
    online_status = models.CharField(max_length=20, choices=ONLINE_STATUS_CHOICES, default='pending')
    audit_opinion = models.TextField(blank=True, null=True)
    auditor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audited_applications'
    )
    audited_at = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'adopt_application'
        ordering = ['-created_at']


class AdoptQuestionnaire(models.Model):
    application = models.OneToOneField(
        AdoptApplication, on_delete=models.CASCADE, related_name='questionnaire'
    )
    answers_json = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adopt_questionnaire'


class AdoptAttachment(models.Model):
    application = models.ForeignKey(AdoptApplication, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.CharField(max_length=30)
    file_url = models.CharField(max_length=500)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adopt_attachment'


class AdoptOfflineVerify(models.Model):
    VERIFY_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]

    application = models.OneToOneField(
        AdoptApplication, on_delete=models.CASCADE, related_name='offline_verify'
    )
    verify_status = models.CharField(max_length=20, choices=VERIFY_STATUS_CHOICES, default='scheduled')
    verify_note = models.TextField(blank=True, null=True)
    verifier = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='offline_verifications'
    )
    verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'adopt_offline_verify'
