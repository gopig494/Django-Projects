# Generated by Django 5.0.4 on 2024-04-12 16:46

import product_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0062_fieldtypescheckl2_file_d'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='file_fun',
            field=models.FileField(default='', upload_to=product_management.models.get_path),
            preserve_default=False,
        ),
    ]
