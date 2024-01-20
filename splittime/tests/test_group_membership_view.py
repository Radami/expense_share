from django.urls import reverse
from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers


class GroupMembershipViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user3 = UserHelpers.create_user(user_name="user3")  # outsider
        cls.user4 = UserHelpers.create_user(user_name="user4")  # user to be added

    def setUp(self):
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, GroupMembershipViewTests.user2)

    def test_add_group_memmber_as_creator(self):
        self.assertEqual(
            self.client.login(username=self.user1.username, password="glassonion123"),
            True,
        )
        data = {"member_email": GroupMembershipViewTests.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(
            reverse("splittime:group_details", args=(self.group1.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GroupMembershipViewTests.user4.username)

    def test_add_group_member_as_member(self):
        self.assertEqual(
            self.client.login(username=self.user2.username, password="glassonion123"),
            True,
        )
        data = {"member_email": GroupMembershipViewTests.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")

        response = self.client.get(
            reverse("splittime:group_details", args=(self.group1.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GroupMembershipViewTests.user4.username)

    def test_add_group_member_as_outsider(self):
        self.assertEqual(
            self.client.login(username=self.user3.username, password="glassonion123"),
            True,
        )
        data = {"member_email": GroupMembershipViewTests.user4.email}
        response = self.client.post(
            reverse("splittime:add_group_member", args=(self.group1.id,)), data=data
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse("splittime:group_details", args=(self.group1.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, GroupMembershipViewTests.user4.username)
