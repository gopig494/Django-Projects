# Generated by Django 5.0.4 on 2024-06-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0045_learnvalidate_uni_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learnvalidate',
            name='uni_field',
            field=models.IntegerField(unique=True),
        ),
    ]