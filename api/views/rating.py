import typing

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import OwnerOrReadOnly
from api.serializers import RatingSerializer
from community.models import Rating

tags = ["api/rating"]


@method_decorator(
    swagger_auto_schema(
        operation_id="Create rating", tags=tags, operation_description="", responses={}
    ),
    name="create",
)
@method_decorator(
    swagger_auto_schema(
        operation_id="List of rating",
        tags=tags,
        operation_description="Выдача рейтинга происходит" " по конкретному объекту",
        responses={},
    ),
    name="list",
)
@method_decorator(
    swagger_auto_schema(
        operation_id="Retrieve the rating",
        tags=tags,
        operation_description="",
        responses={},
    ),
    name="retrieve",
)
@method_decorator(
    swagger_auto_schema(
        operation_id="Update rating", tags=tags, operation_description="", responses={}
    ),
    name="update",
)
@method_decorator(
    swagger_auto_schema(
        operation_id="Partial update rating",
        tags=tags,
        operation_description="",
        responses={},
    ),
    name="partial_update",
)
@method_decorator(
    swagger_auto_schema(
        operation_id="Delete rating", tags=tags, operation_description="", responses={}
    ),
    name="destroy",
)
class RatingViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [OwnerOrReadOnly]

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
