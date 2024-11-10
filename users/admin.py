from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, EmployeePosition


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "full_name", "is_staff", "is_active", "dismissed")
    list_filter = ("is_staff", "is_active", "dismissed", "dismissed_date")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "full_name",
                    "employee_position",
                    "dismissed",
                    "dismissed_date",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "employee_position",
                    "is_staff",
                    "is_active",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "full_name", "employee_position")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)
admin.site.register(EmployeePosition)
