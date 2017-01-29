from django.contrib.auth.models import User
from .. models import Bucketlist, Item
from datetime import datetime
from django.test import TestCase
from rest_framework.test import APITestCase
from. import BaseAPITestCase


class UserTest(APITestCase):
    def test_creating_a_user(self):
        user = User(username='clemn', password='pass123')
        user.save()


class BucketlistTest(BaseAPITestCase):
    def setUp(self):
        self.user = User(username='clemn', password='pass123')
        self.user.save()

    def test_creating_a_bucketlist(self):
        bucket = Bucketlist(name="Cook", created_by=self.user)
        self.assertEqual(bucket.id, None)
        bucket.save()

        #assert attributes
        self.assertFalse(bucket.id == None)
        self.assertEqual(bucket.id, self.user.id)
        self.assertEqual(bucket.name, "Cook")
        self.assertIn('clemn', str(bucket.created_by))
        year = str(datetime.today().year)
        self.assertIn(year, str(bucket.date_created))
        self.assertIn(year, str(bucket.date_modified))

    def test_creating_an_item(self):
        bucket = Bucketlist(name="Play", created_by=self.user)
        self.assertEqual(bucket.id, None)
        bucket.save()
        item = Item(name="Play basketball", bucketlist_id=bucket)
        self.assertEqual(item.id, None)
        item.save()
        self.assertNotEqual(item.id, None)
        self.assertIn("Play", item.name)
        year = str(datetime.today().year)
        self.assertIn(year, str(item.date_created))
        self.assertIn(year, str(item.date_modified))
