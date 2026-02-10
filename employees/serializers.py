from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers

from employees.models import Employee
from shared.utils.email import send_resend_email
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class EmployeeSerializer(serializers.ModelSerializer[Employee]):
    user = CustomUserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user", None)
        original_password = user_data.get("password", get_random_string(length=8))

        # Explicit fields that needs to be automatically set when creating an employee
        user_data["password"] = original_password

        if user_data["role"] != CustomUser.Role.EMPLOYEE:
            raise serializers.ValidationError({"role": "Role must be employee."})

        try:
            # We use an atomic transaction to make sure that all operations are successfull
            # for the objects to be created
            with transaction.atomic():
                user = CustomUser.objects.create_user(**user_data)
                employee = Employee.objects.create(user=user, **validated_data)

                send_resend_email(
                    subject="Your Account Credentials",
                    recipient=user.email,
                    html=f"""
                    <p>Hello,</p>
                    <p>Your account has been created. Here are your login credentials:</p>
                    <p>Email: <strong>{user.email}</strong></p>
                    <p>Temporary Password: <strong>{original_password}</strong></p>
                    <p>Please change your password upon first login.</p>
                    """,
                )
        except Exception as error:
            raise serializers.ValidationError(
                {"error": f"Failed to create account or send email: {str(error)}"}
            )

        return employee

    def update(self, instance: Employee, validated_data):
        user_data = validated_data.pop("user", None)
        user = instance.user

        # Keep in mind that when passing the user fields, it will be in the form of a
        # json dictionary
        #
        # Sample user data:
        # {"user": {"first_name": "some first name", "last_name": "some last name"}}

        if user_data:
            user.email = user_data.get("email", user.email)
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.is_active = user_data.get("is_active", user.is_active)
            user.profile_image = user_data.get("profile_image", user.profile_image)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
