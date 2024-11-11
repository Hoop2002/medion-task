from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager


class EmployeePosition(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField(verbose_name="Почта", blank=False, unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    full_name = models.CharField(verbose_name="ФИО", max_length=255, null=False)
    employee_position = models.ForeignKey(
        verbose_name="Должность",
        to=EmployeePosition,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=False,
    )
    dismissed = models.BooleanField(verbose_name="Уволен", default=False, blank=True)
    dismissed_date = models.DateField(
        verbose_name="Дата увольнения", null=True, blank=True
    )

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
