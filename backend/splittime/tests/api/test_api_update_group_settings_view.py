from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.models import Group


class UpdateGroupSettingsAPIViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="settings_creator")
        cls.outsider = UserHelpers.create_user(user_name="settings_outsider")
        cls.group = GroupHelpers.create_group(creator=cls.creator)

    def test_not_logged_in(self):
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={"group_id": self.group.id, "name": "New Name"},
        )
        self.assertEqual(response.status_code, 401)

    def test_outsider_cannot_update(self):
        UserHelpers.login_user(self.client, self.outsider)
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={"group_id": self.group.id, "name": "Hacked Name"},
        )
        self.assertEqual(response.status_code, 403)

    def test_update_name(self):
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={"group_id": self.group.id, "name": "Updated Name"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Group.objects.get(pk=self.group.id).name, "Updated Name")

    def test_update_description(self):
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={"group_id": self.group.id, "description": "New description"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Group.objects.get(pk=self.group.id).description, "New description")

    def test_update_minimize_balances_setting(self):
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={"group_id": self.group.id, "minimize_balances_setting": True},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Group.objects.get(pk=self.group.id).minimize_balances_setting)

    def test_update_all_settings(self):
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.post(
            reverse("splittime:api_update_group_settings_view"),
            data={
                "group_id": self.group.id,
                "name": "All Updated",
                "description": "All desc",
                "minimize_balances_setting": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        updated = Group.objects.get(pk=self.group.id)
        self.assertEqual(updated.name, "All Updated")
        self.assertEqual(updated.description, "All desc")
        self.assertFalse(updated.minimize_balances_setting)