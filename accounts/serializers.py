from rest_framework import serializers
from .models import User, OtpCode


class UserRegisterSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(
    #     min_length=8, max_length=20, write_only=True, style={"input_type": "password"}
    # )

    class Meta:
        model = User
        fields = ["phone_number", "email", "password", "date_birth","name"]
        extra_kwargs = {
            "password": {"required":True,"write_only": True, "style": {"input_type": "password"}},
            "phone_number": {"required":True,"min_length": 11, "max_length": 11},
            "email": {"required": True, "max_length": 180},
            "name": {"required": True,"max_length":120},
            "date_birth": {"required": True}
        }

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("phone number is duplicate")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("email is duplicate")
        return value


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ["code"]

    # def validate_


class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ("phone_number", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class ChangePasswordAccountSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=20, min_length=8, write_only=True)
    new_password = serializers.CharField(max_length=20, min_length=8, write_only=True)

    # def validate(self, data):
    #     if data.get("new_password") != data.get("current_password"):
    #         raise serializers.ValidationError(detail="password not equal with confirm-password")
    #     return data


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number"]
