# Generated by Django 5.0.4 on 2024-04-12 01:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0027_fieldtypescheckl_suit'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl',
            name='moon_landing',
            field=models.CharField(choices=[(datetime.date(1969, 7, 20), 'Apollo 11 (Eagle)'), (datetime.date(1969, 11, 19), 'Apollo 12 (Intrepid)'), (datetime.date(1971, 2, 5), 'Apollo 14 (Antares)'), (datetime.date(1971, 7, 30), 'Apollo 15 (Falcon)'), (datetime.date(1972, 4, 21), 'Apollo 16 (Orion)'), (datetime.date(1972, 12, 11), 'Apollo 17 (Challenger)')], default=(1972, 12, 11), max_length=100),
            preserve_default=False,
        ),
    ]
