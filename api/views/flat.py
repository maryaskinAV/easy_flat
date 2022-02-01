from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.filters import FlatFilter
from api.serializer import FlatSerializer
from api.permissions import OwnerOrReadOnly

from flat.models import Flat

tags = ['api/flat']


@method_decorator(swagger_auto_schema(operation_id='List of flat',
                                      tags=tags,
                                      operation_description='ViewSet поддерживает фильтрацию по множеству '
                                                            'парамтров при помощи FlatFilter',
                                      responses={},manual_parameters=[openapi.Parameter('booked_days', openapi.IN_QUERY, type="{'upper':'YYYY-MM-DD','lower':'YYYY-MM-DD'}")]), name='list')
@method_decorator(swagger_auto_schema(operation_id='Retrieve the flat',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='retrieve')
@method_decorator(swagger_auto_schema(operation_id='Create flat',
                                      tags=tags,
                                      operation_description='ViewSet для работы с Flat объектами.При создани модели '
                                                            'пользователь является отправителем заявки при помощи '
                                                            'переопределения метода perform_create()',
                                      responses={}),name= 'create')
@method_decorator(swagger_auto_schema(operation_id='Update flat',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='update')
@method_decorator(swagger_auto_schema(operation_id='Partial update flat',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='partial_update')
@method_decorator(swagger_auto_schema(operation_id='Delete flat',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='destroy')
class FlatViewSet(ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [OwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
