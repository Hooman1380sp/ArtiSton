from django.contrib.auth.models import BaseUserManager as BUM


class UserManager(BUM):
    def create_user(self, phone_number: str, password, email: str, date_birth=None, name: str = None):
        if not phone_number:
            raise ValueError('user must have phone number')

        user = self.model(phone_number=phone_number, date_birth=date_birth, name=name,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number: str, password, email: str, date_birth=None, name: str = None):
        user = self.create_user(
            phone_number=phone_number, date_birth=date_birth, name=name, email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.save()
        return user
