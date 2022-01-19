from django.db import models
from django.db.models import Avg
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

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

    def save(self):
        self.clean()
        model_name = ContentType.objects.get(id=self.content_type.id).model_class()
        super().save()
        self.update_avg_rating_for_parent(self.object_id, model_name)

    def delete(self):
        model_name = ContentType.objects.get(id=self.content_type.id).model_class()
        super().delete()
        self.update_avg_rating_for_parent(self.object_id, model_name)

    def clean(self):
        model_name = ContentType.objects.get(id=self.content_type.id).model_class()
        object_exist = get_object_or_404(model_name, pk=self.object_id)
        super().clean()
        if Rating.objects.filter(content_type__pk=self.content_type.id,
                                 object_id=self.object_id, user=self.user).exists():
            raise ValidationError('you have already taken a rating')

    @staticmethod
    def update_avg_rating_for_parent(object_id, model_name: models.Model):
        model = model_name.objects.filter(pk=object_id).annotate(rating_sum=Avg('rating__rating_star')).first()
        model.avg_rating = model.rating_sum
        model.save()
