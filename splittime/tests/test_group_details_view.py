from django.urls import reverse
from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers


class GroupDetailViewTests(TestCase):

    def setUp(self):
        pass

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
        old_group = GroupHelpers.create_group(days=-400)
        url = reverse("splittime:group_details", args=(old_group.id,))
        response = self.client.get(url)
        self.assertContains(response, old_group.name)

    def test_recent_group(self):
        """
        Test that an old group can be viewed
        """
        old_group = GroupHelpers.create_group(days=-5)
        url = reverse("splittime:group_details", args=(old_group.id,))
        response = self.client.get(url)
        self.assertContains(response, old_group.name)

    def test_group_creator_displayed_as_member(self):
        """
        Test that checks group members are displayed
        """
        creator = UserHelpers.create_user()
        member = UserHelpers.create_user()
        group = GroupHelpers.create_group()
        GroupHelpers.add_user_to_group(group, creator)
        GroupHelpers.add_user_to_group(group, member)
        url = reverse("splittime:group_details", args=(group.id,))
        response = self.client.get(url)
        self.assertContains(response, group.name)
        self.assertContains(response, "Members")
        self.assertContains(response, creator.username)
        self.assertContains(response, member.username)
