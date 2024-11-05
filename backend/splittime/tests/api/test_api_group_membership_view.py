from django.db import transaction
from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.serializers import UserSerializer


class GroupMembershipAddAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user3 = UserHelpers.create_user(user_name="user3")  # outsider
        cls.user4 = UserHelpers.create_user(user_name="user4")  # user to be added
        cls.group1 = GroupHelpers.create_group(creator=cls.user1)
        GroupHelpers.add_user_to_group(cls.group1, cls.user2)

    def login(self, user):
        self.assertEqual(
            self.client.login(username=user.username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": user.username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_add_group_member_as_creator(self):
        # login as creator
        self.login(self.user1)

        # test begins
        data = {"member_email": self.user4.email, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_add_group_member_view"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, UserSerializer(self.user4).data)

        response = self.client.get(
            reverse("splittime:api_group_details_view"), data={"groupId": self.group1.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user4.username)

    def test_add_group_member_as_member(self):
        # login as member
        self.login(self.user2)

        # test begins
        data = {"member_email": self.user4.email, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_add_group_member_view"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, UserSerializer(self.user4).data)

        response = self.client.get(
            reverse("splittime:api_group_details_view"), data={"groupId": self.group1.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user4.username)

    @transaction.atomic
    def test_add_group_member_self(self):
        # login as creator
        self.login(self.user1)

        # test begins
        data = {"member_email": self.user1.email, "group_id": self.group1.id}
        with transaction.atomic():
            response = self.client.post(reverse("splittime:api_add_group_member_view"), data=data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, "User is already part of the group")

        with transaction.atomic():
            response = self.client.get(
                reverse("splittime:api_group_details_view"), data={"groupId": self.group1.id}
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.user1.username)

    def test_add_group_member_as_outsider(self):
        # login as outsider
        self.login(self.user4)

        # test begins
        data = {"member_email": self.user4.email, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_add_group_member_view"), data=data)
        self.assertEqual(response.status_code, 403)


class GroupMembershipAPILoginTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1")  # creator
        cls.user2 = UserHelpers.create_user(user_name="user2")  # member
        cls.user3 = UserHelpers.create_user(user_name="user3")  # outsider

    def setUp(self):
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)

    def test_add_group_member_not_logged_in(self):
        data = {"member_email": self.user3.email, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_add_group_member_view"), data=data)
        self.assertEqual(response.status_code, 403)

    def test_delete_group_member_not_logged_in(self):
        data = {"user_id": self.user2.id, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_delete_group_member_view"), data=data)
        self.assertEqual(response.status_code, 401)


class GroupMembershipDeleteViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="user1")  # creator
        cls.member = UserHelpers.create_user(user_name="user2")  # member
        cls.outsider = UserHelpers.create_user(user_name="user3")  # outsider

    def setUp(self):
        self.group1 = GroupHelpers.create_group(creator=self.creator)
        GroupHelpers.add_user_to_group(self.group1, self.member)

    def login(self, user):
        self.assertEqual(
            self.client.login(username=user.username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": user.username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_delete_group_member_as_creator(self):
        # login as creator
        self.login(self.creator)

        # test begins
        data = {"user_id": self.member.id, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_delete_group_member_view"), data=data)
        self.assertEqual(response.status_code, 200)

        # verify user is not in group anymore
        response = self.client.get(
            reverse("splittime:api_group_details_view"), data={"groupId": self.group1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.member.username)

    def test_delete_group_member_as_member(self):
        # login as member
        self.login(self.member)

        # test begins
        data = {"user_id": self.creator.id, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_delete_group_member_view"), data=data)
        self.assertEqual(response.status_code, 200)

        # verify user is not in group anymore
        response = self.client.get(
            reverse("splittime:api_group_details_view"), data={"groupId": self.group1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.creator.username)

    def test_delete_group_member_self(self):
        # login
        self.login(self.member)

        # test begins
        data = {"user_id": self.member.id, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_delete_group_member_view"), data=data)
        self.assertEqual(response.status_code, 403)

    def test_delete_group_member_as_outsider(self):
        # login
        self.login(self.outsider)

        # test begins
        data = {"user_id": self.member.id, "group_id": self.group1.id}
        response = self.client.post(reverse("splittime:api_delete_group_member_view"), data=data)
        self.assertEqual(response.status_code, 403)
