from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = "__all__"

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
        }
        read_only_fields = ("last_login",)

    def create(self, validated_data):
        email = validated_data.get("email")
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        roles = validated_data.pop("roles", None)
        if roles is None:
            raise serializers.ValidationError({"roles": "This field is required."})

        user = CustomUser.objects.create_user(
            email=email, password=validated_data.pop("password", None), **validated_data
        )

        user.roles.set(roles)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("email", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep
