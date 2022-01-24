from . import ApiTestCase
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType

from community.models import Rating


class RatingTestCase(ApiTestCase):

    def setUp(self):
        super().setUp()
        self.rating = Rating.objects.create(object_id=self.flat.id,rating_star=Rating.RatingStar.Two,
                              user=self.admin_user, content_type=ContentType.objects.get_for_model(self.flat))

    def test_rating_list(self):
        url = reverse('rating-list')
        params = f'?content_type={self.rating.content_type.id}&object_id={self.rating.object_id}'
        self.authorize()
        response = self.client.get(url+params)
        self.assertEqual(response.status_code, 200)
