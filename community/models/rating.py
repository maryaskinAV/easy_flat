from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Avg


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

    @classmethod
    def create_rating(self, object_id, rating_star, objects, user):
        object = get_object_or_404(objects, pk=object_id)
        object_type = ContentType.objects.get_for_model(object)
        try:
            Rating.objects.get(content_type__pk=object_type.id, object_id=object_id,
                               user=user)
            raise ValidationError('you have already taken a rating')
        except Rating.DoesNotExist:
            Rating.objects.create(user=user, rating_star=rating_star,
                              content_object=object, object_id=object_id)
        self.create_avg_rating_for_model(object_id,objects)

    @classmethod
    def create_avg_rating_for_model(self,object_id, objects):
        model = objects.objects.filter(pk=object_id).annotate(rating_sum=Avg('rating__rating_star'))[0]
        model.avg_rating = model.rating_sum
        model.save()
