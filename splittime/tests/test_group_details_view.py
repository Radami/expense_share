from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from .helpers import GroupHelpers

class GroupDetailViewTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')

    def test_nonexistent_group(self):
        """
        Test that an old group can be viewed
        """
        url = reverse("splittime:group_details", args=(1234,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_old_group(self):
        """
        Test that an old group can be viewed
        """
        old_group = GroupHelpers.create_group(days = -30)
        url = reverse("splittime:group_details", args=(old_group.id,))
        response = self.client.get(url)
        self.assertContains(response, old_group.name)

    def test_recent_group(self):
        """
        Test that an old group can be viewed
        """
        old_group = GroupHelpers.create_group(days = -5)
        url = reverse("splittime:group_details", args=(old_group.id,))
        response = self.client.get(url)
        self.assertContains(response, old_group.name)