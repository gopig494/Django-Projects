# Generated by Django 5.0.4 on 2024-04-06 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldcheck',
            name='_blank',
            field=models.BinaryField(blank=True),
        ),
    ]
