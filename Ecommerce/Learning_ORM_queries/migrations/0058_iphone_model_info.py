# Generated by Django 5.0.4 on 2024-06-08 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0057_alter_iphone_options_alter_iphonemodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='iphone',
            name='model_info',
            field=models.ManyToManyField(related_name='model_info', to='Learning_ORM_queries.iphonemodel'),
        ),
    ]
