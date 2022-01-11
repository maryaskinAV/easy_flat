from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation


class CustomUser(AbstractUser):
    """
    Основная модель пользователя
    """
    rating = GenericRelation('community.rating', null=True, blank=True)
    avg_rating = models.IntegerField(default=0)


    def __str__(self):
        return self.username
