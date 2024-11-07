from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

from users.models import User, EmployeePosition

from utils.fields import Base64ImageField


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    full_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    auth = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_auth(instance) -> str:
        refresh = RefreshToken.for_user(instance)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    def validate(self, attrs):
        super().validate(attrs)
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        try:
            validate_email(attrs["username"])
            attrs["email"] = attrs["username"]
            email = attrs["username"]
        except ValidationError:
            email = ""
        if password1 != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        _auth_user = None
        if self.context["request"]:
            _auth_user = self.context["request"].user

        if email:
            _user = (
                User.objects.filter(Q(username=attrs["username"]) | Q(email=email))
                .exclude(id=_auth_user.id if _auth_user else None)
                .exists()
            )
        else:
            _user = (
                User.objects.filter(username=attrs["username"])
                .exclude(id=_auth_user.id if _auth_user else None)
                .exists()
            )

        if _user:
            raise serializers.ValidationError(
                {
                    "username": "Пользователь с таким логином или почтой уже зарегистрирован"
                }
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        validated_data["password"] = password
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        validated_data["user"] = user

        return user

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "password1", "password2", "auth")


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EmployeePositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = ("name",)


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
    image = serializers.ImageField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "employee_position",
            "email",
            "image",
            "dismissed",
            "dismissed_date",
        )


class UserEmployeeSerializer(serializers.ModelSerializer):
    employee_position = EmployeePositionListSerializer()
    image = serializers.ImageField()

    class Meta:
        model = User
        fields = UserEmployeeListSerializer.Meta.fields + ("username", "date_joined")


class UserEmployeeUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, max_length=None, use_url=True)
    username = serializers.CharField(required=False)
    employee_position = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "employee_position",
            "email",
            "image",
            "dismissed",
            "dismissed_date",
        )


class UserSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, max_length=None, use_url=True)
    username = serializers.CharField(required=False)
    employee_position = EmployeePositionListSerializer()

    def update(self, instance, validated_data):
        data = self.context["request"].data
        if "password1" in data and "password2" in data:
            password1 = data.pop("password1")
            password2 = data.pop("password2")

            if password1 != password2:
                raise serializers.ValidationError({"message": "Пароли не совпадают"})
            instance.set_password(password1)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "employee_position",
            "email",
            "image",
        )
