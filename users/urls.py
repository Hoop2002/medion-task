from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from users import views

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                # auth urls
                path(
                    "sign_up",
                    views.AuthViewSet.as_view({"post": "sign_up"}),
                    name="sign_up",
                ),
                path(
                    "sign_in",
                    views.AuthViewSet.as_view({"post": "sign_in"}),
                    name="sign_in",
                ),
                path(
                    "refresh-token",
                    views.RefreshViewSet.as_view(),
                    name="token_refresh",
                ),
                # user urls
                path(
                    "user", views.UserViewSet.as_view({"get": "retrieve"}), name="user"
                ),
                path(
                    "user/update",
                    views.UserViewSet.as_view({"put": "update"}),
                    name="user_update",
                ),
                # employee urls
                path(
                    "employee/<int:pk>/",
                    views.EmployeeViewSet.as_view({"get": "retrieve"}),
                    name="employee",
                ),
                path(
                    "employee/list",
                    views.EmployeeViewSet.as_view({"get": "list"}),
                    name="employee_list",
                ),
                path(
                    "employee/<int:pk>/update",
                    views.EmployeeViewSet.as_view({"put": "update"}),
                    name="employee_update",
                ),
            ]
        ),
    )
]
