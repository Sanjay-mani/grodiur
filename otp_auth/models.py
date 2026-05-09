from django.db import models
from django.utils import timezone
from datetime import timedelta
import random


class OTPVerification(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]

    identifier = models.CharField(max_length=255)
    otp_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    otp = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'

    def save(self, *args, **kwargs):
        if not self.pk and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        if timezone.now() > self.expires_at:
            self.status = 'expired'
            self.save()
            return True
        return False

    def validate(self, otp_input):
        if self.is_used:
            return False, "OTP already used"
        if self.is_expired():
            return False, "OTP expired. Request a new one"
        if self.attempts >= 3:
            self.status = 'failed'
            self.save()
            return False, "Maximum attempts exceeded. Please request a new OTP."
        if self.otp != otp_input:
            self.attempts += 1
            self.save()
            remaining = 3 - self.attempts
            return False, f"Wrong OTP! {remaining} attempts left"
        self.is_used = True
        self.status = 'verified'
        self.verified_at = timezone.now()
        self.save()
        return True, "OTP verified!"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.otp_type.upper()} | {self.identifier} | {self.status}"