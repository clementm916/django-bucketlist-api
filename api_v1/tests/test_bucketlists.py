from . import BaseAPITestCase
from .. models import Bucketlist, Item


class TestBucketLists(BaseAPITestCase):
    def test_creating_bucketlist(self):
        # with correct fields
        payload = {'name': 'cook'}
        request = self.test_client.post(
            '/api/v1/bucketlists/', payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 201)
        print(request)
        response = request
        print(response.data)
        self.assertIn('date_created', request.data)
        self.assertIn('date_modified', request.data)
        self.assertIn('cook', str(request.data))

        # with wrong fields
        payload = {'wrongfieldname': 'cook'}
        request = self.test_client.post(
            '/api/v1/bucketlists/', payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data, {"name": ["This field is required."]})

        # with a missing payload
        request = self.test_client.post(
            '/api/v1/bucketlists/', HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 400)
        self.assertIn('name', str(request.data))
        self.assertIn('This field is required', str(request.data))

    def test_retrieving_all_bucketlist(self):
        bucket_1 = Bucketlist(name="Play", created_by=self.user)
        bucket_1.save()
        bucket_2 = Bucketlist(name="Cook", created_by=self.user)
        bucket_2.save()
        bucket_3 = Bucketlist(name="Swim", created_by=self.user)
        bucket_3.save()

        request = self.test_client.get(
            '/api/v1/bucketlists/', HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertIn('Play', str(request.data))
        self.assertIn('Cook', str(request.data))
        self.assertIn('next', str(request.data))

        # test retrieving with a search query
        request = self.test_client.get(
            '/api/v1/bucketlists/?q=play', HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertIn('Play', str(request.data))

    def test_retrieving_a_single_bucketlist(self):
        # an existing bucketlist
        bucket = Bucketlist(name="Play", created_by=self.user)
        bucket.save()
        bucket_id = bucket.id
        request = self.test_client.get(
            '/api/v1/bucketlists/' + str(bucket_id), HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 200)

        # a non-existent bucketlist
        bucket_id = 'notthere'
        request = self.test_client.get(
            '/api/v1/bucketlists/' + str(bucket_id), HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 404)

    def test_editing_a_bucketlist(self):
        # an existing bucketlist
        bucket = Bucketlist(name="Play", created_by=self.user)
        bucket.save()
        bucket_id = bucket.id

        payload = {'name': 'Playing'}
        request = self.test_client.put(
            '/api/v1/bucketlists/' + str(bucket_id), payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertIn('Playing', str(request.data))

        # a non-existent bucketlist
        bucket_id = 'notthere'
        request = self.test_client.put(
            '/api/v1/bucketlists/' + str(bucket_id), payload, HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 404)

    def test_deleting_a_bucketlist(self):
        # an existing bucketlist
        bucket = Bucketlist(name="Play", created_by=self.user)
        bucket.save()
        bucket_id = bucket.id
        request = self.test_client.delete(
            '/api/v1/bucketlists/' + str(bucket_id), HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 204)

        # a non-existent bucketlist
        request = self.test_client.delete(
            '/api/v1/bucketlists/' + str(bucket_id), HTTP_AUTHORIZATION=self.auth, format='json')
        self.assertEqual(request.status_code, 404)
