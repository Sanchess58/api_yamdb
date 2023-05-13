from rest_framework import serializers
from django.contrib.auth import get_user_model 

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        return user

    class Meta:
        model = User
        fields = ( "username", "email", )