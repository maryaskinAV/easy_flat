from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializer import CreateUserSerializers
from user.models import CreateUser


class CreateUserViewSet(ModelViewSet):
    queryset = CreateUser.objects.get_for_activating()
    serializer_class = CreateUserSerializers
    lookup_field = 'uuid'

    @action(detail=True, methods=['POST'], url_path='activation')
    def activation(self, request,uuid, *args, **kwargs):
        order = self.get_object()
        data = order.activate()
        return Response(data)
