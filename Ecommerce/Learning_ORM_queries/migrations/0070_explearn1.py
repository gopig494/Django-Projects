# Generated by Django 5.0.4 on 2024-06-22 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0069_queryexps_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpLearn1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
            ],
        ),
    ]