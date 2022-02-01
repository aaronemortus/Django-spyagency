from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group
from functools import wraps


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Manager(models.Model):
    manager = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='manager',
        limit_choices_to=Q(groups__name='manager')
    )

    def __str__(self):
        return self.manager.email


class Lackey(models.Model):
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lackey = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='lackey',
        null=True,
        blank=True,
        limit_choices_to=Q(groups__name='hitman')
    )

    def __str__(self):
        return self.lackey.email


@receiver(post_save, sender=User)
def add_group_to_user(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='hitman'))


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


@receiver(post_save, sender=User)
@disable_for_loaddata
def create_lackey(sender, instance, created, **kwargs):
    if created:
        lackey = Lackey()
        lackey.lackey = instance
        lackey.save()
