from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import User


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email
