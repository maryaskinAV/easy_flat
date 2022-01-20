from django.shortcuts import reverse
from rest_framework.test import APITestCase
from flat.models import Flat
from user.service import create_token
from user.tests import BaseTestCase



class ApiTestCase(APITestCase, BaseTestCase):

    def setUp(self):
        #todo к тута правильно сделать
        super().setUp()
        self.flat = Flat.objects.create(rooms_count=3, cost=2332,
                            max_guest=32, arena_timeline='OneDay',
                            total_area=23)
        self.flat_two = Flat.objects.create(rooms_count=13, cost=13,
                                   max_guest=13, arena_timeline='OneDay',
                                   total_area=13)

    def authorize(self):
        token = create_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token['token'])

    def test_flat_create(self):
        url = reverse('flat-list')
        data = {'rooms_count': 3, 'cost': 2332, 'max_guest': 32,
                'arena_timeline': 'OneDay', 'total_area': 23}
        self.authorize()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)


    def test_flat_list(self):
        url = reverse('flat-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_flat_get(self):
        url = reverse('flat-detail', args=(self.flat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_flat_filter(self):
        url = reverse('flat-list')
        params = '?cost_min=12&cost_max=15' \
                 '&rooms_count_min=12&rooms_count_max=15' \
                 '&total_area_min=12&total_area_max=15' \
                 '&max_guest_min=12&max_guest_max=15&arena_timeline=OneDay'
        response = self.client.get(url+params)
        self.assertEqual(response.status_code, 200)

