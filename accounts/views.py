from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from .utils import Send_Otp_Code

import random
from .models import OtpCode, User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserForgotPasswordSerializer,
    EditUserProfileSerializer,
    ChangePasswordAccountSerializer,
)
# from .permissions import PermissionEditUserProfile
import time


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    """

    """
    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user = User.objects.create_user(password=ser_data.validated_data.get('password'),
                                        phone_number=ser_data.validated_data.get('phone_number'),
                                        email=ser_data.validated_data.get('email'),
                                        date_birth=ser_data.validated_data.get('date_birth'),
                                        name=ser_data.validated_data.get('name'))
        user.save()
        access = AccessToken.for_user(user)
        access_token = access

        return Response(
            data={"message": str(access_token)},
            status=status.HTTP_201_CREATED,
        )


# class UserVerifyCodeView(APIView):
#     serializer_class = OtpCodeSerializer
#     """
#
#     """
#
#     def post(self, request):
#         ser_data = self.serializer_class(data=request.data)
#         ser_data.is_valid(raise_exception=True)
#         user_session = request.session["user_registration_info"]
#         print(user_session)
#         phone_number = user_session.get("phone_number")
#         code_instance = OtpCode.objects.get(phone_number__iexact=phone_number)
#         code = ser_data.validated_data.get("code")
#         if code == code_instance.code:
#             # if code_instance.created + time.time()
#             User.objects.create_user(**user_session)
#             code_instance.delete()
#             return Response(data={"message": "register user is successful"}, status=status.HTTP_201_CREATED)
#         return Response(data={"message": "code is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    """
    page login view
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_phone = ser_data.validated_data.get("phone_number")
        user_password = ser_data.validated_data.get("password")
        user: User = User.objects.get(phone_number=user_phone)
        if user is not None:
            print(user_phone, "", user_password)
            if not user.is_active:
                return Response({"message": "is Active Your Phone"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if user_phone == user.phone_number:
                    if user.check_password(user_password):
                        login(request, user)
                        return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
                    return Response({"message": "کلمه عبور وارد شده اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "شماره وارد شده اشتباه است"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message": "کاربری با مشخصات شما یافت نشده است"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutView(LoginRequiredMixin, APIView):
    def get(self, request):
        logout(request)
        return redirect("https:/.pythonanywhere.com")


class UserForgotPasswordView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = UserForgotPasswordSerializer
    """
    page forget password
    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user_phone = ser_data.validated_data.get("phone_number")
        user = User.objects.get(phone_number__iexact=user_phone)
        if user is not None:
            random_str = get_random_string(9)
            print(random_str)
            user.set_password(random_str)
            user.save()
            Send_Otp_Code(phone_number=user_phone, message=f"{random_str} [New password] ")
            return Response(data=ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Thr Number is duplicate "}, status=status.HTTP_406_NOT_ACCEPTABLE)
