import typing

from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from community.models import Rating


class ListRatingMixin:

    def list(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        model_name: Model = ContentType.objects.get_for_id(
            id=self.request.GET["content_type"]
        )
        object_id = self.request.GET["object_id"]
        data = Rating.objects.filter(object_id=object_id, content_type=model_name)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)