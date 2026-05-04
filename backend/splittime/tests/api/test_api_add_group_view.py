from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import UserHelpers
from splittime.models import Group, GroupMembership


class AddGroupAPIViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="add_group_u1")

    def test_not_logged_in(self):
        response = self.client.post(
            reverse("splittime:api_add_group"),
            data={"name": "Test Group", "description": "Test description"},
        )
        self.assertEqual(response.status_code, 401)

    def test_add_group_valid(self):
        UserHelpers.login_user(self.client, self.user1)
        response = self.client.post(
            reverse("splittime:api_add_group"),
            data={"name": "New Group", "description": "A test group"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "New Group")
        self.assertEqual(response.data["creator"], self.user1.username)
        group = Group.objects.get(name="New Group")
        self.assertTrue(GroupMembership.objects.filter(group=group, member=self.user1).exists())

    def test_add_group_missing_name_returns_400(self):
        UserHelpers.login_user(self.client, self.user1)
        response = self.client.post(
            reverse("splittime:api_add_group"),
            data={"description": "Missing name"},
        )
        self.assertEqual(response.status_code, 400)

    def test_add_group_missing_description_returns_400(self):
        UserHelpers.login_user(self.client, self.user1)
        response = self.client.post(
            reverse("splittime:api_add_group"),
            data={"name": "No description"},
        )
        self.assertEqual(response.status_code, 400)