from django.test import TestCase

from ..helpers import GroupHelpers, UserHelpers


class GroupModelTests(TestCase):

    def setUp(self):
        self.user_helpers = UserHelpers()
        self.group_helpers = GroupHelpers()
        self.creator = self.user_helpers.create_user()

    def test_was_created_recently_with_future_group(self):
        """
        was_created_recently() returns False for questions whose creation_date is
        in the future
        """
        future_group = self.group_helpers.create_group(days=1)
        self.assertIs(future_group.was_created_recently(), False)

    def test_was_created_recently_with_old_group(self):
        """
        was_created_recently() returns False for questions whose creation_date is
        too old
        """
        future_group = self.group_helpers.create_group(days=-400)
        self.assertIs(future_group.was_created_recently(), False)

    def test_was_created_recently_with_recent_group(self):
        """
        was_created_recently() returns True for questions whose creation_date is
        in the last 365 days
        """
        future_group = self.group_helpers.create_group(days=-5)
        self.assertIs(future_group.was_created_recently(), True)
