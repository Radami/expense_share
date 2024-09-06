from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.serializers import GroupSerializer


class GroupIndexAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="testuser")

    def setUp(self):

        self.assertEqual(
            self.client.login(username=self.user1.username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": self.user1.username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_no_group(self):
        """
        If no group exists, an appropriate message is displayed
        """
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_old_group(self):
        """
        If an old group exists, no groups are displayed
        """
        GroupHelpers.create_group(days=-400, creator=self.user1)
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_recent_group(self):
        """
        If a recent group exists, display it
        """
        group = GroupHelpers.create_group(days=-5, creator=self.user1)
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data[0], GroupSerializer(group).data)

    def test_old_and_recent_group(self):
        """
        If a recent and old group exists, display only the recent one
        """
        GroupHelpers.create_group(days=-400, creator=self.user1)
        group_recent = GroupHelpers.create_group(days=-5, creator=self.user1)
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], GroupSerializer(group_recent).data)
