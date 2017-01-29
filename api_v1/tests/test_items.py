import django
django.setup()

from .. models import Bucketlist, Item
from . import BaseAPITestCase


class TestItem(BaseAPITestCase):
    def setUp(self):
        super(TestItem, self).setUp()
        self.bucket = Bucketlist(name="Play", created_by=self.user)
        self.bucket.save()
        self.bucket_id = self.bucket.id

    def test_creating_an_item(self):
        payload = {'name': 'Cook'}
        request = self.test_client.post(
            '/api/v1/bucketlists/' + str(self.bucket_id) + '/items/', payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 201)

    def test_editing_an_item(self):
        # an existing item
        item = Item(name="Play tabletennis", bucketlist_id=self.bucket)
        item.save()
        item_id = item.id
        payload = {'name': 'Play soccer'}

        request = self.test_client.put(
            '/api/v1/bucketlists/' + str(self.bucket_id) + '/items/' + str(item_id), payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertIn('Play soccer', str(request.data))
        # a non-existent item
        item_id = 'notthere'
        request = self.test_client.put(
            '/api/v1/bucketlists/' + str(self.bucket_id) + '/items/' + str(item_id), payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 404)
        # an empty name

    def test_deleting_an_item(self):
        # an existing item
        item = Item(name="Play tabletennis", bucketlist_id=self.bucket)
        item.save()
        item_id = item.id
        payload = {'name': 'Play soccer'}

        request = self.test_client.delete(
            '/api/v1/bucketlists/' + str(self.bucket_id) + '/items/' + str(item_id), payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 204)

        # a non-existent item
