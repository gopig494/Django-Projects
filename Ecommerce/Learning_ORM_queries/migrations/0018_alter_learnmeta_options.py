# Generated by Django 5.0.4 on 2024-05-28 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0017_alter_learnmeta_table_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learnmeta',
            options={'default_manager_name': 'custom_manager'},
        ),
    ]
