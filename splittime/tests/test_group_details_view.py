from django.urls import reverse
from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers


class GroupDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user2 = UserHelpers.create_user(user_name="user3")  # outsider
        cls.old_group = GroupHelpers.create_group(days=-400, creator=cls.user1)
        cls.new_group = GroupHelpers.create_group(days=-5, creator=cls.user1)
        GroupHelpers.add_user_to_group(cls.old_group, cls.user2)

    def setUp(self):
        self.assertEqual(
            self.client.login(
                username=GroupDetailViewTests.user1.username,
                password="glassonion123",
            ),
            True,
        )

    def test_nonexistent_group(self):
        url = reverse("splittime:group_details", args=(1234,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_old_group(self):
        url = reverse(
            "splittime:group_details", args=(GroupDetailViewTests.old_group.id,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GroupDetailViewTests.old_group.name)

    def test_recent_group(self):
        url = reverse(
            "splittime:group_details", args=(GroupDetailViewTests.new_group.id,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GroupDetailViewTests.new_group.name)

    def test_group_creator_displayed_as_member(self):
        url = reverse(
            "splittime:group_details", args=(GroupDetailViewTests.old_group.id,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GroupDetailViewTests.old_group.name)
        self.assertContains(response, "Members")
        self.assertContains(response, GroupDetailViewTests.user1.username)
        self.assertContains(response, GroupDetailViewTests.user2.username)


class GroupDetailViewPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # outsider
        cls.group = GroupHelpers.create_group(creator=cls.user1)

    def test_group_details_login_required(self):
        url = reverse(
            "splittime:group_details",
            args=(GroupDetailViewPermissionTests.group.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            "/splittime/login?next=/splittime/group/"
            + str(GroupDetailViewPermissionTests.group.id)
            + "/",
            response.url,
        )

    def test_group_permission_as_outsider(self):
        self.assertEqual(
            self.client.login(
                username=GroupDetailViewPermissionTests.user2.username,
                password="glassonion123",
            ),
            True,
        )
        url = reverse(
            "splittime:group_details",
            args=(GroupDetailViewPermissionTests.group.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
