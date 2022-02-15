from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, \
                                  UpdateModelMixin, \
                                  DestroyModelMixin

from api.mixins import CreateRatingMixin, ListRatingMixin
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
class RatingViewSet(CreateRatingMixin,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    ListRatingMixin,
                    GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [OwnerOrReadOnly]
