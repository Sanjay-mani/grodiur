from django.contrib import admin
from .models import OTPVerification


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'identifier', 'otp_type', 'otp',
        'status', 'attempts', 'is_used',
        'created_at', 'expires_at', 'verified_at'
    ]
    list_filter = ['otp_type', 'status', 'is_used']
    search_fields = ['identifier', 'otp']
    readonly_fields = ['otp', 'created_at', 'expires_at', 'verified_at']
    ordering = ['-created_at']