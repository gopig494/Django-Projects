# Generated by Django 5.0.4 on 2024-04-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0058_fieldtypescheckl2_duration_f'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='email_f',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
