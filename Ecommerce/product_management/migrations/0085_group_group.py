# Generated by Django 5.0.4 on 2024-04-15 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0084_group_uuids'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, to='product_management.group'),
        ),
    ]