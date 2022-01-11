from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializer import PasswordChangeOrderSerializer
from user.models import PasswordChangeOrder


class PasswordChangeOrderViewSet(ModelViewSet):
    queryset = PasswordChangeOrder.objects.get_for_activating()
    serializer_class = PasswordChangeOrderSerializer
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'], url_path='activation')
    def activation(self, request,uuid, *args, **kwargs):
        order = self.get_object()
        data = order.activate()
        return Response(data)
