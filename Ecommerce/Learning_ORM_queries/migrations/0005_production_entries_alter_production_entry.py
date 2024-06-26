# Generated by Django 5.0.4 on 2024-04-30 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0004_production_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='entries',
            field=models.ManyToManyField(to='Learning_ORM_queries.entry'),
        ),
        migrations.AlterField(
            model_name='production',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_forign', to='Learning_ORM_queries.entry'),
        ),
    ]
