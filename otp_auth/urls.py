from django.urls import path
from .views import (
    SendEmailOTPView,
    VerifyEmailOTPView,
    SendPhoneOTPView,
    VerifyPhoneOTPView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('send-email-otp/', SendEmailOTPView.as_view()),
    path('verify-email-otp/', VerifyEmailOTPView.as_view()),
    path('send-phone-otp/', SendPhoneOTPView.as_view()),
    path('verify-phone-otp/', VerifyPhoneOTPView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]