# Generated by Django 5.0 on 2024-01-03 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splittime', '0009_alter_debt_ratio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='debt',
            old_name='ratio',
            new_name='shares',
        ),
    ]
