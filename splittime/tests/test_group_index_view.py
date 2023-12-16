from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from .helpers import GroupHelpers

class GroupIndexViewTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')

    def test_no_group(self):
        """
        If no group exists, an appropriate message is displayed
        """
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No groups are available")
        self.assertQuerySetEqual(response.context["latest_group_list"], [])
        
    def test_old_group(self):
        """
        If an old group exists, no groups are displayed
        """
        GroupHelpers.create_group(days = -30)
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No groups are available")
        self.assertQuerySetEqual(response.context["latest_group_list"], [])

    def test_recent_group(self):
        """
        If a recent group exists, display it
        """
        group = GroupHelpers.create_group(days = -5)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"], [group])

    def test_old_and_recent_group(self):
        """
        If a recent and old group exists, display onyl the recent one
        """
        GroupHelpers.create_group(days = -30)
        group_recent = GroupHelpers.create_group(days = -5)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"], [group_recent])

    def test_two_recent_groups(self):
        """
        The index page might display multiple groups in reverse order of creation
        """
        group_first = GroupHelpers.create_group(days = -5)
        group_second = GroupHelpers.create_group(days = -2)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"],
                                 [group_second, group_first])
