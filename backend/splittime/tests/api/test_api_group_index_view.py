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
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data[0], GroupSerializer(group).data)

    def test_old_and_recent_group(self):
        """
        If a recent and old group exists, display only the recent one
        """
        GroupHelpers.create_group(days=-400, creator=self.user1)
        group_recent = GroupHelpers.create_group(days=-5, creator=self.user1)
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], GroupSerializer(group_recent).data)

    def test_two_recent_groups(self):
        """
        The index page might display multiple groups in reverse order of creation
        """
        group_first = GroupHelpers.create_group(days=-300, creator=self.user1)
        group_second = GroupHelpers.create_group(days=-200, creator=self.user1)
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 2)
        self.assertIn(GroupSerializer(group_first).data, response.data)
        self.assertIn(GroupSerializer(group_second).data, response.data)


class GroupIndexViewNotLoggedInTests(APITestCase):
    """
    Test that all group API requests return 401 if user is not logged in
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")
        cls.group1 = GroupHelpers.create_group(creator=cls.user1)

    def setUp(self):
        pass

    def test_index_view(self):
        """
        Trying to access the index view without being logged in should return 401
        """
        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 401)

    def test_add_group(self):
        """
        Trying to access the add group view without being logged in should return 200 and the
        login url
        """
        response = self.client.post(reverse("splittime:api_add_group"))
        self.assertEqual(response.status_code, 401)

    def test_delete_group(self):
        """
        Trying to access the delete group view without being logged in should return 200 and the
        login url
        """
        response = self.client.post(
            reverse(
                "splittime:api_delete_group",
            ),
            data={"id": self.group1.id},
        )
        self.assertEqual(response.status_code, 401)


class GroupPermissionsTests(APITestCase):
    """
    Test that permissions are respected when accessing group index views
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")
        cls.user2 = UserHelpers.create_user(user_name="user2")
        cls.user3 = UserHelpers.create_user(user_name="user3")
        cls.group1 = GroupHelpers.create_group(creator=cls.user1)
        cls.group2 = GroupHelpers.create_group(creator=cls.user2)
        cls.group3 = GroupHelpers.create_group(creator=cls.user3)
        cls.group2_1 = GroupHelpers.create_group(creator=cls.user2)
        GroupHelpers.add_user_to_group(cls.group2, cls.user3)

    def setUp(self):
        pass

    def login(self, username):
        self.assertEqual(
            self.client.login(username=username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_index_with_1_group_as_creator(self):
        """
        Index view with creator and 1 group should return that group and nothing else
        """
        self.login(self.user1.username)

        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertIn(GroupSerializer(self.group1).data, response.data)

    def test_index_with_2_groups_as_creator(self):
        """
        Index view with 2 groups as creator should return both groups and nothing else
        """
        self.login(self.user2.username)

        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 2)
        self.assertIn(GroupSerializer(self.group2).data, response.data)
        self.assertIn(GroupSerializer(self.group2_1).data, response.data)

    def test_index_with_2_groups_as_creator_and_member(self):
        """
        Index view with 2 groups (one as creator and one as member) should return both groups
        and nothing else
        """
        self.login(self.user3.username)

        response = self.client.get(reverse("splittime:api_index_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 2)
        self.assertIn(GroupSerializer(self.group3).data, response.data)
        self.assertIn(GroupSerializer(self.group2).data, response.data)

    def test_delete_grpup_as_creator(self):
        """
        Delete group should work for a group where the user is the creator
        """
        self.login(self.user1.username)
        response = self.client.post(
            reverse(
                "splittime:api_delete_group",
            ),
            data={"id": self.group1.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_group_with_no_permission(self):
        """
        Delete group should return 403 for groups where the user is not the creator
        """
        self.login(self.user1.username)
        response = self.client.post(
            reverse(
                "splittime:api_delete_group",
            ),
            data={"id": self.group2.id},
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_group_as_member(self):
        """
        Delete group should return 403 for a group where the user is just member
        """
        self.login(self.user3.username)
        response = self.client.post(
            reverse(
                "splittime:api_delete_group",
            ),
            data={"id": self.group2.id},
        )
        self.assertEqual(response.status_code, 403)
