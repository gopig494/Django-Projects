# Generated by Django 5.0.4 on 2024-04-16 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0093_rename_parent_field_parent_parent_field_me'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
    ]
