# Generated by Django 5.0.4 on 2024-06-04 03:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0046_alter_learnvalidate_uni_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnvalidate',
            name='learn_m',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='Learning_ORM_queries.learnmodel'),
            preserve_default=False,
        ),
    ]