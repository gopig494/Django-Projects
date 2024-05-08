# Generated by Django 5.0.4 on 2024-05-08 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0006_alter_author_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20, verbose_name='Current City')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learning_ORM_queries.blog', verbose_name='Blog')),
                ('parent_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Learning_ORM_queries.location')),
            ],
        ),
    ]
