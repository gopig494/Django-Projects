# Generated by Django 5.0.4 on 2024-04-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0060_fieldtypescheckl2_file_f'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtypescheckl2',
            name='file_f',
            field=models.FileField(upload_to='files'),
        ),
    ]
