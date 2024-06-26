# Generated by Django 5.0.4 on 2024-06-24 02:28

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0087_childlearnmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='childlearnmanager',
            managers=[
                ('child_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
