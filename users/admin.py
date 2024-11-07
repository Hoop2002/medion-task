from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from users.models import User, EmployeePosition


class UserAdmin(BaseUserAdmin):
    search_fields = ("email", "username", "last_name", "first_name", "user_id")

    list_display = (
        "username",
        "image_tag",
        "email",
        "user_id",
        "full_name",
        "first_name",
        "last_name",
    )

    list_filter = (
        "date_joined",
        "is_active",
        "is_superuser",
    )

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{}" style="width: 60px; height: 60px; border-radius: 50%;"/>'.format(
                    obj.image.url
                )
            )


UserAdmin.fieldsets = UserAdmin.fieldsets + (
    (
        "Информация о сотруднике",
        {"fields": ("full_name", "employee_position")},
    ),
)

admin.site.register(User, UserAdmin)
admin.site.register(EmployeePosition)
