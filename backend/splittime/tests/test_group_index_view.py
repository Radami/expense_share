from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

from .helpers import GroupHelpers, UserHelpers
from ..serializers import GroupSerializer


class GroupIndexViewTests(TestCase):
    """
    Tests business logic of retrieving old and new groups
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="testuser")

    def setUp(self):
        self.assertEqual(
            self.client.login(username=self.user1.username, password="glassonion123"),
            True,
        )

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
        GroupHelpers.create_group(days=-400, creator=self.user1)
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No groups are available")
        self.assertQuerySetEqual(response.context["latest_group_list"], [])

    def test_recent_group(self):
        """
        If a recent group exists, display it
        """
        group = GroupHelpers.create_group(days=-5, creator=self.user1)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"], [group])

    def test_old_and_recent_group(self):
        """
        If a recent and old group exists, display only the recent one
        """
        GroupHelpers.create_group(days=-400, creator=self.user1)
        group_recent = GroupHelpers.create_group(days=-5, creator=self.user1)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"], [group_recent])

    def test_two_recent_groups(self):
        """
        The index page might display multiple groups in reverse order of creation
        """
        group_first = GroupHelpers.create_group(days=-300, creator=self.user1)
        group_second = GroupHelpers.create_group(days=-200, creator=self.user1)
        response = self.client.get(reverse("splittime:index"))
        self.assertQuerySetEqual(response.context["latest_group_list"], [group_second, group_first])


class GroupIndexViewNotLoggedInTests(TestCase):
    """
    Test that all views redirect to the login page if user is not logged in
    """

    def setUp(self):
        pass

    def test_index_view(self):
        """
        Trying to access the index view without being logged in should return 200 and the
        login url
        """
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual("/splittime/login?next=/splittime/", response.url)
        self.assertEqual(response.status_code, 302)

    def test_add_group(self):
        """
        Trying to access the add group view without being logged in should return 200 and the
        login url
        """
        response = self.client.post(reverse("splittime:add_group"))
        self.assertEqual("/splittime/login?next=/splittime/add_group", response.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_group(self):
        """
        Trying to access the delete group view without being logged in should return 200 and the
        login url
        """
        response = self.client.post(reverse("splittime:delete_group", args=("1",)))
        self.assertEqual("/splittime/login?next=/splittime/group/1/delete_group", response.url)
        self.assertEqual(response.status_code, 302)


class GroupIndexViewPermissionsTests(TestCase):
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

    def test_index_with_1_group_as_creator(self):
        """
        Index view with creator and 1 group should return that group and nothing else
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user1.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_group_list"],
            [GroupIndexViewPermissionsTests.group1],
        )

    def test_index_with_2_groups_as_creator(self):
        """
        Index view with 2 groups as creator should return both groups and nothing else
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user2.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_group_list"],
            [
                GroupIndexViewPermissionsTests.group2_1,
                GroupIndexViewPermissionsTests.group2,
            ],
        )

    def test_index_with_2_groups_as_creator_and_member(self):
        """
        Index view with 2 groups (one as creator and one as member) should return both groups
        and nothing else
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user3.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.get(reverse("splittime:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_group_list"],
            [GroupIndexViewPermissionsTests.group3, self.group2],
        )

    def test_delete_grpup_as_creator(self):
        """
        Delete group should work for a group where the user is the creator
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user1.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group",
                args=(GroupIndexViewPermissionsTests.group1.id,),
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/")

    def test_delete_group_with_no_permission(self):
        """
        Delete group should return 403 for groups where the user is not the creator
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user1.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group",
                args=(GroupIndexViewPermissionsTests.group2.id,),
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_group_as_member(self):
        """
        Delete group should return 403 for a group where the user is just member
        """
        self.assertEqual(
            self.client.login(
                username=GroupIndexViewPermissionsTests.user3.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group",
                args=(GroupIndexViewPermissionsTests.group2.id,),
            )
        )
        self.assertEqual(response.status_code, 403)


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
