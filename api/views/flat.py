from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import FlatFilter
from api.serializer import FlatSerializer
from api.permissions import OwnerOrReadOnly

from flat.models import Flat


class FlatViewSet(ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [OwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
