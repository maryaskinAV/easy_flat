from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from api.serializer import RatingSerializer
from api.permissions import OwnerOrReadOnly
from community.models import Rating
from flat.models import Flat
from user.models import CustomUser


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [OwnerOrReadOnly]

    @action(detail=False, methods=['POST'], url_path='create_rating')
    def create_rating(self, request, *args, **kwargs):
        object_id = request.data['object_id']
        content_type = ContentType.objects.get_for_id(id=request.data['content_type'])
        rating_star = request.data['rating']
        user = request.user
        rating = Rating(rating_star=rating_star, user=user, object_id=object_id, content_type=content_type)
        rating.save()
        return Response({'status': 200})

    #todo
    """сделать выдачу всех моделей рейтинга относительно родительской модели
     можно ли для этой задачи использовать метод list т.к возможность получать 
     все модели рейтинга не имеет смысла"""
