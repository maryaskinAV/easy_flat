from . import ApiTestCase
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType

from community.models import Rating


class RatingTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.rating = Rating.objects.create(object_id=self.flat.id, rating_star=Rating.RatingStar.Two,
                                            user=self.admin_user,
                                            content_type=ContentType.objects.get_for_model(self.flat))

    def test_rating_list(self):
        url = reverse('rating-list')
        params = f'?content_type={self.rating.content_type.id}&object_id={self.rating.object_id}'
        self.authorize(self.admin_user)
        response = self.client.get(url + params)
        self.assertEqual(response.status_code, 200)

    def test_rating_get(self):
        url = reverse('rating-detail', args=(self.rating.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rating_post(self):
        url = reverse('rating-list')
        self.authorize(self.quest)
        data = {'object_id': self.flat.id, 'content_type': ContentType.objects.get_for_model(self.flat).id,
                'rating_star': Rating.RatingStar.Free}
        response = self.client.post(url+'create_rating/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_rating_patch(self):
        url = reverse('rating-detail', args=(self.rating.id,))
        self.authorize(self.admin_user)
        data = {'rating_star': Rating.RatingStar.Four}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)



