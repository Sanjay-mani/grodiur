from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


def send_otp_email(email, otp):
    try:
        send_mail(
            subject='Your Grodiur OTP Code 🛒',
            message=f'''Hello!

Your Grodiur verification code is:

━━━━━━━━━━━━
    {otp}
━━━━━━━━━━━━

✅ Valid for 5 minutes only
❌ Do not share with anyone
🔒 Max 3 attempts allowed

Happy Shopping! 🥦
Team Grodiur''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent to {email}")
        return True, "OTP sent successfully"
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False, f"Failed to send email: {str(e)}"


def send_otp_sms(phone, otp):
    """Send OTP via Twilio SMS."""
    try:
        from twilio.rest import Client
        
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_phone = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        if not all([account_sid, auth_token, from_phone]):
            logger.warning("Twilio credentials not fully set — skipping SMS")
            return True, f"OTP generated (Twilio not configured): {otp}"

        client = Client(account_sid, auth_token)
        
        # Format the phone number (ensure it has country code, assuming +91 for India if not present)
        formatted_phone = phone
        if not formatted_phone.startswith('+'):
            formatted_phone = f'+91{formatted_phone}'
            
        message = client.messages.create(
            body=f"""
🛒 Grodiur Login Verification

Use OTP {otp} to continue.

Expires in 5 minutes.

For security reasons, never share this code with anyone.
""",
            from_=from_phone,
            to=formatted_phone
        )
        
        logger.info(f"OTP SMS sent to {phone} | SID: {message.sid}")
        return True, "OTP sent to phone"
        
    except Exception as e:
        logger.error(f"Twilio SMS error: {e}")
        return False, f"SMS service error: {str(e)}"