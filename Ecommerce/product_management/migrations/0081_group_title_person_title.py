# Generated by Django 5.0.4 on 2024-04-15 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0080_group_person_group_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
