from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class MeSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "role")

    def get_role(self, obj: User) -> str | None:
        profile: UserProfile | None = getattr(obj, "builder_profile", None)
        if profile is None:
            return None
        return profile.role
