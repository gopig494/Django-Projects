# Generated by Django 5.0.4 on 2024-06-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0077_dbmathfunc_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbmathfunc',
            name='title',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
    ]
