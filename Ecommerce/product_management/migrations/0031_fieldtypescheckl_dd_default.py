# Generated by Django 5.0.4 on 2024-04-12 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0030_alter_fieldtypescheckl_suit'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl',
            name='dd_default',
            field=models.CharField(blank=True, db_default='i am de default', max_length=100),
        ),
    ]
