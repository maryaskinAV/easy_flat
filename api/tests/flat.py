from django.shortcuts import reverse

from flat.models import Flat

from . import ApiTestCase


class FlatTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_flat_post(self) -> None:
        url = reverse("flat-list")
        data = {
            "rooms_count": 3,
            "cost": 2332,
            "max_guest": 32,
            "arena_timeline": "OneDay",
            "total_area": 23,
        }
        self.authorize(self.admin_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_flat_list(self) -> None:
        url = reverse("flat-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flat_get(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flat_filter(self) -> None:
        url = reverse("flat-list")
        data = {
            "cost_min": 12,
            "cost_max": 10000,
            "rooms_count_min": 2,
            "rooms_count_max": 4,
            "total_area_min": 12,
            "total_area_max": 40,
            "max_guest_min": 12,
            "max_guest_max": 40,
            "arena_timeline": "OneDay",
            "booked_days": {"upper": "2012-12-1", "lower": "2012-12-2"},
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_patch(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        data = {
            "rooms_count": 3422,
            "cost": 54353,
            "max_guest": 3122,
            "arena_timeline": "OneDay",
            "total_area": 2432,
        }
        self.authorize(self.admin_user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_delete(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        self.authorize(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Flat.objects.filter(id=self.flat.id).exists())
