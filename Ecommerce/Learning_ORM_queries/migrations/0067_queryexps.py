# Generated by Django 5.0.4 on 2024-06-16 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0066_searchkey_search_vector_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryExps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
