# Generated by Django 5.0.4 on 2024-04-12 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0033_alter_fieldtypescheckl_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtypescheckl',
            name='dd_index',
            field=models.CharField(blank=True, db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='fieldtypescheckl',
            name='year',
            field=models.CharField(blank=True, choices=[(None, 'Please Select Choice..'), ('2012', '2k12'), ('2k13', '2k13')], default='FZS', max_length=100, null=True),
        ),
    ]
