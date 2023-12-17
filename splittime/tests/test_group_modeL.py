import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Group
from .helpers import GroupHelpers

class GroupModelTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')

    def test_was_created_recently_with_future_group(self):
        """
        was_created_recently() returns False for questions whose creation_date is 
        in the future
        """
        future_group = GroupHelpers.create_group(days = 1)
        self.assertIs(future_group.was_created_recently(), False)

    def test_was_created_recently_with_old_group(self):
        """
        was_created_recently() returns False for questions whose creation_date is
        too old
        """
        future_group = GroupHelpers.create_group(days = -400)
        self.assertIs(future_group.was_created_recently(), False)

    def test_was_created_recently_with_recent_group(self):
        """
        was_created_recently() returns True for questions whose creation_date is 
        in the last 365 days
        """
        future_group = GroupHelpers.create_group(days = -5)
        self.assertIs(future_group.was_created_recently(), True)



