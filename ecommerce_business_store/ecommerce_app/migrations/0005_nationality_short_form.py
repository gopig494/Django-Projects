# Generated by Django 4.2.5 on 2023-09-20 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_customer_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='nationality',
            name='short_form',
            field=models.CharField(default='IND', max_length=10),
        ),
    ]
