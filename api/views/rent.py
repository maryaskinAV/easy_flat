from rest_framework.viewsets import ModelViewSet
from flat.models import Renting

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializer import RentSerializer
from api.permissions import OwnerOrReadOnly

tags = ['api/rent']


@method_decorator(swagger_auto_schema(operation_id='List of rent',
                                      tags=tags,
                                      operation_description='Выдача бронировок происходит'
                                                            ' по запросившему пользователю',
                                      responses={}), name='list')
@method_decorator(swagger_auto_schema(operation_id='Retrieve the rent',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='retrieve')
@method_decorator(swagger_auto_schema(operation_id='Update rent',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='update')
@method_decorator(swagger_auto_schema(operation_id='Partial update rent',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='partial_update')
@method_decorator(swagger_auto_schema(operation_id='Delete rent',
                                      tags=tags,
                                      operation_description='',
                                      responses={}), name='destroy')
@method_decorator(swagger_auto_schema(operation_id='Create rent',
                                      tags=tags,
                                      operation_description='Бронировку может сделать '
                                                            'только авторизованный пользователь',
                                      responses={}, manual_parameters=[
        openapi.Parameter('lease_duration', openapi.IN_QUERY,description="{'upper':'YYYY-MM-DD','lower':'YYYY-MM-DD'}",type="date")]),
                  name='create')
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
        # При получении бронировок квартир пользователь получит только свои бронировки
        queryset = Renting.objects.filter(user=self.request.user)
        return queryset
