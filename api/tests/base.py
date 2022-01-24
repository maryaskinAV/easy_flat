from rest_framework.test import APITestCase
from user.service import create_token
from user.tests import BaseTestCase

from flat.models import Flat


class ApiTestCase(APITestCase, BaseTestCase):

    def setUp(self):
        super().setUp()
        self.flat = Flat.objects.create(rooms_count=3, cost=2332,
                                        max_guest=32, arena_timeline='OneDay',
                                        total_area=23, owner=self.admin_user)

    def authorize(self,user):
        token = create_token(user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token['token'])
