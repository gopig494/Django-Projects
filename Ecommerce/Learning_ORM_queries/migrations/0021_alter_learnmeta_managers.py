# Generated by Django 5.0.4 on 2024-05-28 02:22

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0020_alter_learnmeta_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='learnmeta',
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
