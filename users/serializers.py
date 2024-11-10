from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

from users.models import User, EmployeePosition

from utils.fields import Base64ImageField


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField()
    full_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    auth = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_auth(instance) -> str:
        refresh = RefreshToken.for_user(instance)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    def _is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def _user_exists(self, email):
        return User.objects.filter(email=email).exists()

    def validate(self, attrs):
        super().validate(attrs)

        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        email = attrs.get("email")
        if not self._is_valid_email(email):
            raise serializers.ValidationError(
                {"email": "Некорректный адрес электронной почты."}
            )

        if password1 != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if len(password1) < 8:
            raise serializers.ValidationError(
                {"password": "Пароль должен содержать минимум 8 символов."}
            )

        if self._user_exists(email):
            raise serializers.ValidationError(
                {"email": "Пользователь с таким логином уже зарегистрирован"}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        validated_data["password"] = password
        validated_data["username"] = validated_data["email"]
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        validated_data["user"] = user

        return user

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password1", "password2", "auth")


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            message = (
                "Пожалуйста, введите корректные имя пользователя и"
                " пароль учётной записи. Оба поля могут быть чувствительны"
                " к регистру."
            )
            raise serializers.ValidationError({"message": message})
        attrs["user"] = user
        return attrs


class AccessTokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class EmployeePositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = (
            "id",
            "name",
        )


class EmployeePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = EmployeePositionListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class UserEmployeeListSerializer(serializers.ModelSerializer):
    employee_position = EmployeePositionListSerializer()

    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "employee_position",
            "dismissed",
            "dismissed_date",
        )


class UserEmployeeSerializer(serializers.ModelSerializer):
    employee_position = EmployeePositionListSerializer()

    class Meta:
        model = User
        fields = UserEmployeeListSerializer.Meta.fields + ("user_id", "date_joined")


class UserEmployeeUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    employee_position = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "full_name",
            "employee_position",
            "email",
            "dismissed",
            "dismissed_date",
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    employee_position = EmployeePositionListSerializer(required=False, read_only=True)
    password1 = serializers.CharField(required=False)
    password2 = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        data = self.context["request"].data
        if "password1" in data and "password2" in data:
            password1 = data["password1"]
            password2 = data["password2"]

            if password1 != password2:
                raise serializers.ValidationError({"message": "Пароли не совпадают"})
            instance.set_password(password1)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "full_name",
            "employee_position",
            "email",
            "password1",
            "password2",
        )
