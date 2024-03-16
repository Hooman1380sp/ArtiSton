# from django.contrib.auth import login
# from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from .utils import Send_Otp_Code

import random
from .models import OtpCode, User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserForgotPasswordSerializer,
    OtpCodeSerializer,
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
            data={"Jwt_Token": str(access_token)},
            status=status.HTTP_201_CREATED,
        )


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
            if not user.is_active:
                return Response({"message": "Is Not Active Your Phone"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user_phone == user.phone_number:
                if user.check_password(user_password):
                    # login(request, user)
                    access = AccessToken.for_user(user)
                    access_token = access
                    return Response({"message": str(access_token)}, status=status.HTTP_202_ACCEPTED)
                return Response({"message": "password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "phone_number is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message": "we can.t find any user with your Specifications"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)


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
            # random_int = get_random_string(9)
            random_int = random.randint(1000, 9999)
            # print(random_str)
            # todo (send code for user)
            # user.set_password(random_str)
            # user.save()
            Send_Otp_Code(phone_number=user_phone, message=f"{random_int} [OTP]. One Time Password ")
            OtpCode.objects.create(phone_number=user_phone,code=random_int)
            return Response(data=ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Thr Number is duplicate "}, status=status.HTTP_406_NOT_ACCEPTABLE)


class OtpCodeViewPost(APIView):
    serializer_class = OtpCodeSerializer
    """

    """

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        phone_number = vd["phone_number"]
        code_instance = OtpCode.objects.get(phone_number__iexact=phone_number)
        code = vd["code"]
        if code == code_instance.code:
            expiration_time = code_instance.created + timedelta(seconds=59)
            if timezone.now() > expiration_time:
                code_instance.delete()
                return Response({'message': 'the code has expired'}, status=status.HTTP_408_REQUEST_TIMEOUT)
            code_instance.delete()
            access = AccessToken.for_user(User.objects.get(phone_number=phone_number))
            access_token = access
            return Response(data={"Jwt_Token":str(access_token)}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "code is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
