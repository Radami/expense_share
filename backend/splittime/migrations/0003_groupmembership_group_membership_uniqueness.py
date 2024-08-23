# Generated by Django 5.0 on 2023-12-08 23:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splittime', '0002_group_creation_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='groupmembership',
            constraint=models.UniqueConstraint(fields=('group', 'member'), name='group_membership_uniqueness'),
        ),
    ]