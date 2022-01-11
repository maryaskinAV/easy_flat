from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


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
        content_type = request.data['content_type']
        rating = request.data['rating']
        user = request.user
        if content_type == 'flat':
            Rating.create_rating(object_id, rating, objects=Flat, user=user)
        if content_type == 'user':
            Rating.create_rating(object_id, rating, objects=CustomUser, user=user)
        return Response({'status': 200})
