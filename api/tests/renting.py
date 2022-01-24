import json

from . import ApiTestCase
from django.shortcuts import reverse
from psycopg2.extras import DateRange
from flat.models import Renting


class RentingTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.renting = Renting.objects.create(flat=self.flat, user=self.admin_user,
                                              count_guest=31,
                                              lease_duration=DateRange(lower='2012-11-01', upper='2012-11-10',
                                                                       bounds='[)'))

    def test_renting_create(self):
        url = reverse('rent-list')
        self.authorize()
        data = {'flat': self.flat.id, 'user': self.admin_user,
                'count_guest': 31, 'lease_duration': json.dumps({'upper': '2012-12-01',
                                                                 'lower': '2012-11-10', 'bounds': '[)'})}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_renting_edit(self):
        url = reverse('rent-detail', args=(self.renting.id,))
        self.authorize()
        data = {'count_guest': 22, 'lease_duration': json.dumps({'upper': '2012-12-01',
                                                                 'lower': '2012-11-10', 'bounds': '[)'})}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_renting_delete(self):
        url = reverse('rent-detail', args=(self.renting.id,))
        self.authorize()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Renting.objects.filter(id=self.renting.id).exists())

    def test_renting_get(self):
        url = reverse('rent-detail', args=(self.renting.id,))
        self.authorize()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flat_list(self):
        url = reverse('rent-list')
        self.authorize()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
