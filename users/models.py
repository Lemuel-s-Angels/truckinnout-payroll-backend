import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, validate_email
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from shared.validators import validate_image


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError({"email": "Please specify an email address."})

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = CustomUser.Role.SUPER_ADMIN
        user.first_name = "SUPER"
        user.last_name = "ADMIN"
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ADMIN = "admin", "Admin"
        EMPLOYEE = "employee", "Employee"
        OPERATING_PERSONNEL = "operating_personnel", "Operating Personnel"

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email])
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=50, choices=Role.choices, blank=False, null=False
    )
    profile_image = models.ImageField(
        upload_to="user-media",
        validators=[
            validate_image,
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
        ],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
