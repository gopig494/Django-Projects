# Generated by Django 5.0.3 on 2024-04-05 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0005_fieldcheck__db_col'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldcheck',
            name='_db_col',
            field=models.BigIntegerField(db_column='auto_db_col', default=8),
        ),
    ]
