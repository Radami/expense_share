from django.urls import reverse
from django.test import TestCase, TransactionTestCase

from .helpers import GroupHelpers, UserHelpers


class GroupMembershipAddViewTests(TransactionTestCase):
    def setUp(self):
        self.user1 = UserHelpers.create_user(user_name="user1")  # creator
        self.user2 = UserHelpers.create_user(user_name="user2")  # member
        self.user3 = UserHelpers.create_user(user_name="user3")  # outsider
        self.user4 = UserHelpers.create_user(user_name="user4")  # user to be added
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)

    def test_add_group_memmber_as_creator(self):
        self.assertEqual(
            self.client.login(
                username=self.user1.username,
                password="glassonion123",
            ),
            True,
        )
        data = {"member_email": self.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user4.username)

    def test_add_group_member_as_member(self):
        self.assertEqual(
            self.client.login(
                username=self.user2.username,
                password="glassonion123",
            ),
            True,
        )
        data = {"member_email": self.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user4.username)

    def test_add_group_member_self(self):
        self.assertEqual(
            self.client.login(
                username=self.user1.username,
                password="glassonion123",
            ),
            True,
        )
        data = {"member_email": self.user1.email}

        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)

    def test_add_group_member_as_outsider(self):
        self.assertEqual(
            self.client.login(
                username=self.user3.username,
                password="glassonion123",
            ),
            True,
        )
        data = {"member_email": self.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 403)


class GroupMembershipViewsLoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user3 = UserHelpers.create_user(user_name="user3")  # outsider

    def setUp(self):
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)

    def test_add_group_member_not_logged_in(self):
        data = {"member_email": GroupMembershipViewsLoginTests.user3.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            "/splittime/login?next=/splittime/group/" + str(self.group1.id) + "/add_member",
            response.url,
        )

    def test_delete_group_member_not_logged_in(self):
        response = self.client.post(
            reverse(
                "splittime:delete_group_member",
                args=(
                    self.group1.id,
                    GroupMembershipViewsLoginTests.user2.id,
                ),
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            "/splittime/login?next=/splittime/group/"
            + str(self.group1.id)
            + "/delete_group_member/"
            + str(GroupMembershipViewsLoginTests.user2.id),
            response.url,
        )


class GroupMembershipDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user3 = UserHelpers.create_user(user_name="user3")  # outsider

    def setUp(self):
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, GroupMembershipDeleteViewTests.user2)

    def test_delete_group_member_as_creator(self):
        self.assertEqual(
            self.client.login(
                username=self.user1.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group_member",
                args=(
                    self.group1.id,
                    GroupMembershipDeleteViewTests.user2.id,
                ),
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user2.username)

    def test_delete_group_member_as_member(self):
        self.assertEqual(
            self.client.login(
                username=self.user2.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group_member",
                args=(
                    self.group1.id,
                    GroupMembershipDeleteViewTests.user1.id,
                ),
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user1.username)

    def test_delete_group_member_self(self):
        self.assertEqual(
            self.client.login(
                username=self.user2.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group_member",
                args=(
                    self.group1.id,
                    GroupMembershipDeleteViewTests.user2.id,
                ),
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(reverse("splittime:group_details", args=(self.group1.id,)))
        self.assertEqual(response.status_code, 403)

    def test_delete_group_member_as_outsider(self):
        self.assertEqual(
            self.client.login(
                username=self.user3.username,
                password="glassonion123",
            ),
            True,
        )
        response = self.client.post(
            reverse(
                "splittime:delete_group_member",
                args=(
                    self.group1.id,
                    GroupMembershipDeleteViewTests.user2.id,
                ),
            ),
        )
        self.assertEqual(response.status_code, 403)
