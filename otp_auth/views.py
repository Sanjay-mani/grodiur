from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from .models import OTPVerification
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .utils import send_otp_email, send_otp_sms
from accounts.models import UserProfile


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class SendEmailOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        # Rate limit: 10 requests in 2 minutes
        recent = OTPVerification.objects.filter(
            identifier=email,
            otp_type='email',
            created_at__gte=timezone.now() - timezone.timedelta(minutes=2)
        ).count()

        if recent >= 10:
            return Response(
                {'error': 'Too many requests. Wait 2 minutes.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Invalidate (delete) old unverified OTPs for this email
        OTPVerification.objects.filter(
            identifier=email,
            otp_type='email',
            status='pending'
        ).delete()

        # Create OTP
        import random
        otp = str(random.randint(100000, 999999))
        
        otp_obj = OTPVerification.objects.create(
            identifier=email,
            otp_type='email',
            otp=otp,
            ip_address=get_client_ip(request)
        )

        success, message = send_otp_email(email, otp)
        if not success:
            otp_obj.delete()
            return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': f'OTP sent to {email}',
            'expires_in': 300
        })


class VerifyEmailOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        otp_input = serializer.validated_data.get('otp')

        try:
            otp_obj = OTPVerification.objects.filter(
                identifier=email,
                otp_type='email',
                is_used=False,
                status='pending'
            ).latest('created_at')
        except OTPVerification.DoesNotExist:
            return Response(
                {'error': 'No active OTP. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, message = otp_obj.validate(otp_input)
        if not is_valid:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email}
        )
        if created:
            UserProfile.objects.create(user=user)

        # Log the user into the Django session
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({
            'message': 'Login successful!',
            'tokens': get_tokens(user),
            'user': {
                'id': user.id,
                'email': email,
                'username': user.username,
            },
            'is_new_user': created
        })


class SendPhoneOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data.get('phone')

        # Rate limit: 10 requests in 2 minutes
        recent = OTPVerification.objects.filter(
            identifier=phone,
            otp_type='phone',
            created_at__gte=timezone.now() - timezone.timedelta(minutes=2)
        ).count()

        if recent >= 10:
            return Response(
                {'error': 'Too many requests. Wait 2 minutes.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Invalidate (delete) old unverified OTPs for this phone number
        OTPVerification.objects.filter(
            identifier=phone,
            otp_type='phone',
            status='pending'
        ).delete()

        # Create OTP
        import random
        otp = str(random.randint(100000, 999999))
        
        otp_obj = OTPVerification.objects.create(
            identifier=phone,
            otp_type='phone',
            otp=otp,
            ip_address=get_client_ip(request)
        )

        success, message = send_otp_sms(phone, otp)
        if not success:
            otp_obj.delete()
            return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': f'OTP sent to {phone}',
            'expires_in': 300
        })


class VerifyPhoneOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data.get('phone')
        otp_input = serializer.validated_data.get('otp')

        try:
            otp_obj = OTPVerification.objects.filter(
                identifier=phone,
                otp_type='phone',
                is_used=False,
                status='pending'
            ).latest('created_at')
        except OTPVerification.DoesNotExist:
            return Response(
                {'error': 'No active OTP. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, message = otp_obj.validate(otp_input)
        if not is_valid:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            username=phone,
            defaults={'email': ''}
        )
        
        # Ensure profile exists and has the phone number
        profile, p_created = UserProfile.objects.get_or_create(user=user)
        if p_created or not profile.phone:
            profile.phone = phone
            profile.save()

        # Log the user into the Django session
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({
            'message': 'Login successful!',
            'tokens': get_tokens(user),
            'user': {
                'id': user.id,
                'phone': phone,
            },
            'is_new_user': created
        })
