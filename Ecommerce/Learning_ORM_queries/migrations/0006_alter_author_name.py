# Generated by Django 5.0.4 on 2024-05-03 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0005_production_entries_alter_production_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]