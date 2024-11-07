from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login
from users.serializers import (
    UserCreateSerializer,
    SignInSerializer,
    UserSerializer,
    EmployeePositionListSerializer,
    EmployeePositionSerializer,
    UserEmployeeListSerializer,
    UserEmployeeSerializer,
    UserEmployeeUpdateSerializer
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User


@extend_schema(tags=["auth-v1"])
class RefreshViewSet(TokenRefreshView):
    pass


@extend_schema(tags=["auth-v1"])
class AuthViewSet(GenericViewSet):
    queryset = User.objects
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "sign_up":
            return UserCreateSerializer
        return SignInSerializer

    def sign_up(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = self.get_serializer(user)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        else:
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def sign_in(self, request, *args, **kwargs):
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            message = (
                "Пожалуйста, введите корректные имя пользователя и"
                " пароль учётной записи. Оба поля могут быть чувствительны"
                " к регистру."
            )
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        refresh_token = RefreshToken.for_user(user)
        response = Response(
            data={
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
            }
        )
        return response


@extend_schema(tags=["user-v1"])
class UserViewSet(ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=["employee-v1"])
class EmployeeViewSet(ModelViewSet):
    queryset = User.objects
    serializer_class = UserEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return UserEmployeeListSerializer
        if self.action == "update":
            return UserEmployeeUpdateSerializer
        return UserEmployeeSerializer
