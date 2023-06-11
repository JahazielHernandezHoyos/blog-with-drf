from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.accounts.models import Account, Comments, Entrace, Tags
from apps.utils.shortcuts import get_object_or_none


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ("deleted", "password", "last_login", "is_superuser", "groups")
        extra_kwargs = {
            "uuid": {"read_only": True},
            "username": {"read_only": True},
            "is_active": {"read_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        email = validated_data.get("email")
        if Account.objects.filter(email=email, deleted=False).exists():
            raise serializers.ValidationError({"email": "El correo ya está en uso"})
        account = Account.objects.create_user(**validated_data)
        return account


class AccountRegisterSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        exclude = (
            "deleted",
            "password",
            "last_login",
            "is_superuser",
            "groups",
            "is_active",
            "role",
        )
        extra_kwargs = {
            "raw_password": {"write_only": True},
            "validation_code": {"read_only": True},
            "is_active": {"read_only": True},
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=64)
    password = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        username = data.get("username")
        if not Account.objects.filter(username=username, deleted=False).exists():
            raise serializers.ValidationError({"username": "El usuario no existe"})
        if not user:
            raise serializers.ValidationError({"password": "La clave no es válida"})
        if not hasattr(user, "account"):
            raise serializers.ValidationError(
                {"error": "No tiene permisos para entrar aquí"}
            )
        self.context["user"] = user
        return data

    def create(self, data):
        user = self.context["user"]
        token = get_object_or_none(Token, user=user)
        if token:
            token.delete()
        token, created = Token.objects.update_or_create(user=user)
        user = AccountSerializer(user.account)
        return user.data, token.key


class BaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = "__all__"
        extra_kwargs = {
            "uuid": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "deleted": {"read_only": True},
        }


class CommentsSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = Comments
        fields = "__all__"
        extra_kwargs = {
            "account": {"read_only": True},
            "entrace": {"read_only": True},
        }


class EntranceSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = Entrace
        fields = "__all__"
        extra_kwargs = {
            "account": {"read_only": True},
            "entrace": {"read_only": True},
        }
