from django.contrib.auth import get_user_model
from django.forms import ValidationError
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            "username",
            "email"
        )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError({"message": "недопустимый username"})
        return username


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.UUIDField()

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
