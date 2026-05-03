from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splittime', '0010_rename_ratio_debt_shares'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='minimize_balances_setting',
            field=models.BooleanField(default=False),
        ),
    ]
