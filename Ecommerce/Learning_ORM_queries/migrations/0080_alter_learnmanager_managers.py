# Generated by Django 5.0.4 on 2024-06-23 05:48

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0079_learnmanager'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='learnmanager',
            managers=[
                ('my_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]