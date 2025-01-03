from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path(
                    "sign_up/",
                    views.AuthViewSet.as_view({"post": "sign_up"}),
                    name="sign_up",
                ),
                path(
                    "sign_in/",
                    views.AuthViewSet.as_view({"post": "sign_in"}),
                    name="sign_in",
                ),
                path(
                    "refresh-token/",
                    views.RefreshViewSet.as_view(),
                    name="token_refresh",
                ),
                path(
                    "user/", views.UserViewSet.as_view({"get": "retrieve"}), name="user"
                ),
                path(
                    "user/update/",
                    views.UserViewSet.as_view({"put": "update"}),
                    name="user_update",
                ),
                path(
                    "employee/<int:pk>/",
                    views.EmployeeViewSet.as_view({"get": "retrieve"}),
                    name="employee",
                ),
                path(
                    "employee/",
                    views.EmployeeViewSet.as_view({"get": "list"}),
                    name="employee_list",
                ),
                path(
                    "employee/update/<int:pk>/",
                    views.EmployeeViewSet.as_view({"put": "update"}),
                    name="employee_update",
                ),
                path(
                    "employee/drop/<int:pk>/",
                    views.EmployeeViewSet.as_view({"delete": "destroy"}),
                    name="employee_destroy",
                ),
                path(
                    "employee_position/",
                    views.EmployeePositionViewSet.as_view({"get": "list"}),
                    name="employee_position_list",
                ),
                path(
                    "employee_position/<int:pk>/",
                    views.EmployeePositionViewSet.as_view({"get": "retrieve"}),
                    name="employee_position_retrieve",
                ),
            ]
        ),
    )
]

urlpatterns += router.urls
