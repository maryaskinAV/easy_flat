import typing

from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.contenttypes.models import ContentType

from community.models import Rating
# TODO Ты говорил разделить рейтинг пользователя и квартиры в отдельные миксины или что то типо такого.
#  Как это понять и сделать ?

class CreateRatingMixin:

    def create(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        object_id: int = request.data["object_id"]
        content_type = ContentType.objects.get_for_id(id=request.data["content_type"])
        rating_star = request.data["rating_star"]
        user = request.user
        rating = Rating(
            rating_star=rating_star,
            user=user,
            object_id=object_id,
            content_type=content_type,
        )
        rating.save()
        return Response({"status": 200})
