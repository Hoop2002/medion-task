from drf_spectacular.utils import extend_schema
from django.contrib.auth import login
from users.serializers import (
    UserCreateSerializer,
    SignInSerializer,
    UserSerializer,
    EmployeePositionListSerializer,
    EmployeePositionSerializer,
    UserEmployeeListSerializer,
    UserEmployeeSerializer,
    UserEmployeeUpdateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import ChangeUser, DeleteUser, IsNotAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from users.models import User, EmployeePosition
from users.filters import EmployeeFilter


@extend_schema(tags=["auth-v1"])
class RefreshViewSet(TokenRefreshView):
    pass


@extend_schema(tags=["auth-v1"])
class AuthViewSet(GenericViewSet):
    queryset = User.objects
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "sign_up":
            return [IsNotAuthenticated()]
        return super().get_permissions()

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            refresh_token = RefreshToken.for_user(user)
            response = Response(
                data={
                    "access": str(refresh_token.access_token),
                    "refresh": str(refresh_token),
                }
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["user-v1"])
class UserViewSet(ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@extend_schema(tags=["employee-v1"])
class EmployeeViewSet(ModelViewSet):
    queryset = User.objects
    serializer_class = UserEmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EmployeeFilter
    search_fields = ("full_name", "email")

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)

    def get_permissions(self):
        if self.action == "update":
            return [ChangeUser()]
        elif self.action == "destroy":
            return [DeleteUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return UserEmployeeListSerializer
        if self.action == "update":
            return UserEmployeeUpdateSerializer
        return UserEmployeeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["employee-v1"])
class EmployeePositionViewSet(ModelViewSet):
    queryset = EmployeePosition.objects.all()
    serializer_class = EmployeePositionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeePositionListSerializer
        if self.action == "retrieve":
            return EmployeePositionSerializer
        return EmployeePositionSerializer
