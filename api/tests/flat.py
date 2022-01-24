from . import ApiTestCase
from django.shortcuts import reverse
from flat.models import Flat


class FlatTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()

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
        response = self.client.get(url + params)
        self.assertEqual(response.status_code, 200)

    def test_flat_edit(self):
        url = reverse('flat-detail', args=(self.flat.id,))
        data = {'rooms_count': 3422, 'cost': 54353, 'max_guest': 3122,
                'arena_timeline': 'OneDay', 'total_area': 2432}
        self.authorize()
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_delete(self):
        url = reverse('flat-detail', args=(self.flat.id,))
        self.authorize()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Flat.objects.filter(id=self.flat.id).exists())
