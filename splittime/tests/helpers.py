import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Group

class GroupHelpers():
    
    def create_group(group_name = "Default name",
                 group_description = "Default description",
                 days = 0):
        """
        Creates a group with the given description an published the number of days offset
        to now (negative for past, positive for future)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        user = User.objects.get(username='testuser')
        return Group.objects.create(name = group_name,
                                    creator = user,
                                    description = group_description,
                                    creation_date = time)