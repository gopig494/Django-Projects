# Generated by Django 5.0.4 on 2024-04-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0068_fieldtypescheckl2_img_f_fieldtypescheckl2_img_h_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='json_ob',
            field=models.JSONField(default={'model': 'json'}, null=True),
        ),
    ]
