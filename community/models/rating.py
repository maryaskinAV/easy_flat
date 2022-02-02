from django.db import models
from django.db.models import Avg

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import typing

if not typing.TYPE_CHECKING:
    from user.models import CustomUser


class Rating(models.Model):
    """
    Создание рейтинга для привязанного объекта
    """
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='rating')
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, null=True)

    class RatingStar(models.IntegerChoices):
        One = 1
        Two = 2
        Free = 3
        Four = 4
        Five = 5

    rating_star = models.IntegerField(choices=RatingStar.choices)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        model_name = ContentType.objects.get(id=self.content_type.id).model_class()
        object_exist = get_object_or_404(model_name, pk=self.object_id)
        super().clean()
        if Rating.objects.filter(content_type__pk=self.content_type.id,
                                 object_id=self.object_id, user=self.user).exists() and self.id is None:
            raise ValidationError('you have already taken a rating')


@receiver(post_delete, sender=Rating)
@receiver(post_save, sender=Rating)
def update_avg_rating_for_parent(sender: Rating, instance: Rating, **kwargs):
    model_name = ContentType.objects.get(id=instance.content_type.id).model_class()
    model = model_name.objects.filter(pk=instance.object_id).annotate(rating_sum=Avg('rating__rating_star')).first()
    model.avg_rating = model.rating_sum
    model.save()