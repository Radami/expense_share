# Generated by Django 5.0 on 2023-12-08 23:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splittime', '0003_groupmembership_group_membership_uniqueness'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('currency', models.CharField(max_length=3)),
                ('amount', models.FloatField(max_length=9)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_group', to='splittime.group')),
            ],
        ),
    ]
