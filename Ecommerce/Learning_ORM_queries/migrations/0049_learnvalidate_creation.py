# Generated by Django 5.0.4 on 2024-06-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0048_learnvalidate_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnvalidate',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, default='2024-06-04 00:00:00'),
            preserve_default=False,
        ),
    ]