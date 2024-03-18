from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    OtpCodeViewPost,
    UserForgotPasswordView,
    EditUserProfileView,
    ChangePasswordAccountView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("otp/", OtpCodeViewPost.as_view(), name="otp_code"),
    path("forgot-password/", UserForgotPasswordView.as_view(), name="forget_pass"),
    path("edit-profile/", EditUserProfileView.as_view(), name="edit_profile"),
    path("change-password/", ChangePasswordAccountView.as_view(), name="change_password"),

]
