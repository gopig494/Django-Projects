# Generated by Django 5.0.4 on 2024-05-28 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0021_alter_learnmeta_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learnmeta',
            options={'base_manager_name': 'custom_manager', 'default_manager_name': 'custom_manager'},
        ),
    ]
