# Generated by Django 5.0.4 on 2024-04-12 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0029_remove_fieldtypescheckl_moon_landing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtypescheckl',
            name='suit',
            field=models.IntegerField(choices=[(None, 'Please Choose Choice.'), (1, 'Diamond'), (2, 'Spade'), (3, 'Heart'), (4, 'Club')]),
        ),
    ]
