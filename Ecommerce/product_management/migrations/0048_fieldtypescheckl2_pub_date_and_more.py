# Generated by Django 5.0.4 on 2024-04-12 02:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0047_fieldtypescheckl2_many_alter_fieldtypescheckl2_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl2',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fieldtypescheckl2',
            name='many',
            field=models.ManyToManyField(to='product_management.fieldtypescheckl', unique_for_date='pub_date'),
        ),
    ]
