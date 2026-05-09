from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=15, required=False)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(
                "Please provide email or phone number"
            )
        return data


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    otp = serializers.CharField(max_length=6, min_length=6)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be 6 digits")
        return value

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(
                "Please provide email or phone number"
            )
        return data