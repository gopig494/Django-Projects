# Generated by Django 5.0.4 on 2024-04-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0057_fieldtypescheckl2_datetime_cr'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='duration_f',
            field=models.DurationField(null=True),
        ),
    ]
