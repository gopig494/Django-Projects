# Generated by Django 4.2.5 on 2024-03-15 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0005_nationality_short_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=13),
        ),
    ]