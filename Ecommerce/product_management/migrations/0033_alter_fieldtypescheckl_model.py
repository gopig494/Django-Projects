# Generated by Django 5.0.4 on 2024-04-12 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0032_alter_fieldtypescheckl_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtypescheckl',
            name='model',
            field=models.CharField(choices=[(None, 'Please Select Choice..'), ('FZS', 'fzs'), ('FZX', 'fzx')], default='FZS', max_length=100),
        ),
    ]