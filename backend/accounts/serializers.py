from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class UserSerializerWithToken(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

    def getToken(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
