# Generated by Django 5.0.4 on 2024-04-12 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0056_alter_fieldtypescheckl2_datetime_now'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='datetime_cr',
            field=models.DateTimeField(auto_now_add=True, default='2024-04-12'),
            preserve_default=False,
        ),
    ]
