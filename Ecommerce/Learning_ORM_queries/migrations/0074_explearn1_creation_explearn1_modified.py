# Generated by Django 5.0.4 on 2024-06-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0073_explearn1_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='explearn1',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, default='2024-06-22 12:24:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='explearn1',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
