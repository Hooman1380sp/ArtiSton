from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


# TZ#$usBt22DRnC6z

class User(AbstractBaseUser):
    name = models.CharField(max_length=120, null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True, db_index=True, verbose_name="Phone Number")
    email = models.EmailField(max_length=180, verbose_name="Email", unique=True)
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    is_active = models.BooleanField(default=True, verbose_name="active")
    date_birth = models.DateField(verbose_name="Date Birth", null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        app_label = "accounts"
        # db_table = "User"
        db_table_comment = "custom user model with row attribute(AbstractBaseUser)"
        verbose_name = "User"
        verbose_name_plural = "Users"


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, db_index=True, verbose_name="Phone Number")
    code = models.PositiveSmallIntegerField(verbose_name="Code")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created Date_Time")

    class Meta:
        ordering = ["-created"]
        app_label = "accounts"
        # db_table = "OTP_Code"
        db_table_comment = "otp table is for verify code of number 1000 to 9999"
        verbose_name = "Active Code"
        verbose_name_plural = "Active codes"

    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"
