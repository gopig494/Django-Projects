# Generated by Django 5.0.4 on 2024-06-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_rename_name_testmigrate_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestMigrate2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=100)),
            ],
        ),
    ]
