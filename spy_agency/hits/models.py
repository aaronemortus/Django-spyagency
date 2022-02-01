from django.db import models
from django.db.models import Q

from users.models import User


class Hit(models.Model):
    STATUS_CHOICES = [
        ('assigned','Assigned'),
        ('failed','Failed'),
        ('completed','Completed'),
    ]
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignee',
        limit_choices_to=Q(groups__name__in=['hitman', 'manager'])
    )
    description = models.TextField()
    target = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='assigned'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator',
        limit_choices_to=Q(groups__name__in=['bigboss', 'manager'])
    )

    def __str__(self):
        return self.target
