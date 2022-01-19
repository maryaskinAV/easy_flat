from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from flat.models import Renting

from api.serializer import RentSerializer
from api.permissions import OwnerOrReadOnly


class RentingViewSet(ModelViewSet):
    """
    Viweset для создания бронировки квартиры и показа всех личных бронировок пользователю
    """
    permission_classes = [OwnerOrReadOnly]
    serializer_class = RentSerializer
    queryset = Renting.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # При получении бронировок квартир пользователь получит только сои бронировки
        queryset = Renting.objects.filter(user=self.request.user)
        return queryset
