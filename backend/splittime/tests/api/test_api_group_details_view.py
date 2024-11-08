from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers


class GroupDetailsAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="creator")  # creator
        cls.member = UserHelpers.create_user(user_name="member")  # member
        cls.old_group = GroupHelpers.create_group(days=-400, creator=cls.creator)
        cls.new_group = GroupHelpers.create_group(days=-5, creator=cls.creator)
        GroupHelpers.add_user_to_group(cls.old_group, cls.member)

    def setUp(self):
        self.assertEqual(
            self.client.login(username=self.creator.username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": self.creator.username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_no_group(self):
        data = {"group_id": 1234}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 404)

    def test_old_group(self):
        data = {"group_id": self.old_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.old_group.name)

    def test_recent_group(self):
        data = {"group_id": self.new_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.new_group.name)

    def test_group_creator_displayed_as_member(self):
        data = {"group_id": self.old_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.old_group.name)
        self.assertContains(response, "group_members")
        self.assertContains(response, self.creator.username)
        self.assertContains(response, self.member.username)


class GroupDetailsAPIViewPermissionTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="creator")  # creator
        cls.outsider = UserHelpers.create_user(user_name="outsider")  # outsider
        cls.group = GroupHelpers.create_group(creator=cls.creator)

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

    def test_group_details_login_required(self):
        data = {"group_id": self.group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 401)

    def test_group_details_permission_as_outsider(self):
        self.login(self.outsider)
        data = {"group_id": self.group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 401)
