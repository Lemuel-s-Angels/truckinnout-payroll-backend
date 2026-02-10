from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from shared.models import BaseModel


# Create your models here.
class Employee(BaseModel):
    class EmployeeTypes(models.TextChoices):
        DRIVER = "driver", "Driver"
        HELPER = "helper", "Helper"
        STAFF = "staff", "Staff"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
    )
    type = models.CharField(
        max_length=50, choices=EmployeeTypes.choices, blank=False, null=False
    )
    philhealth_number = models.CharField(
        max_length=80, blank=False, null=False, unique=True
    )
    pag_ibig_number = models.CharField(
        max_length=80, blank=False, null=False, unique=True
    )
    sss_number = models.CharField(max_length=80, blank=False, null=False, unique=True)
    drivers_license_number = models.CharField(
        max_length=80, blank=False, null=False, unique=True
    )
    mobile_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r"^(09|\+639)\d{9}$",
                message="Phone number must be a valid Philippine mobile number (e.g., 09171234567 or +639171234567).",
            )
        ],
        unique=True,
    )
