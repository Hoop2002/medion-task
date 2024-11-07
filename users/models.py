from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.functions import generate_upload_name
import uuid


class EmployeePosition(models.Model):
    name = models.CharField(verbose_name="Название", max_length=256)
    employee_position_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class User(AbstractUser):
    full_name = models.CharField(verbose_name="ФИО", max_length=256, null=False)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(
        upload_to=generate_upload_name,
        verbose_name="Фото пользователя",
        null=True,
        blank=False,
    )
    employee_position = models.ForeignKey(
        verbose_name="Должность",
        to=EmployeePosition,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=False,
    )
    dismissed = models.BooleanField(verbose_name="Уволен", default=False, blank=False)
    dismissed_date = models.DateField(
        verbose_name="Дата увольнения", null=True, blank=False
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
