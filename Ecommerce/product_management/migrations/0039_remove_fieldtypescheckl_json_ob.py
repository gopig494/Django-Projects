# Generated by Django 5.0.4 on 2024-04-12 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0038_alter_fieldtypescheckl_checking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldtypescheckl',
            name='json_ob',
        ),
    ]
