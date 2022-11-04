from django.contrib.auth.base_user import BaseUserManager
from delivery_management.constants import DELIVERYMAN, PROFESSIONNAL, TEAM


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email.lower(), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(password, **extra_fields)

    def teams(self):
        return self.get_queryset().filter(user_type=TEAM)

    def deliverymen(self):
        return self.get_queryset().filter(user_type=DELIVERYMAN)

    def professionnals(self):
        return self.get_queryset().filter(user_type=PROFESSIONNAL)

    def active(self):
        return self.get_queryset().filter(is_active=True)
