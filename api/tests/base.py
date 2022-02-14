from rest_framework.test import APITestCase

from flat.models import Flat
from user.models import CustomUser
from user.service import create_token
from user.tests import BaseTestCase


class ApiTestCase(APITestCase, BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.flat = Flat.objects.create(
            rooms_count=3,
            cost=2332,
            max_guest=32,
            arena_timeline="OneDay",
            total_area=23,
            owner=self.admin_user,
        )

    def authorize(self, user: CustomUser) -> None:
        token = create_token(user)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
