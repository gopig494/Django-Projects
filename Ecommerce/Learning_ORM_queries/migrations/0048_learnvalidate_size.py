# Generated by Django 5.0.4 on 2024-06-04 16:42

import Learning_ORM_queries.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0047_learnvalidate_learn_m'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnvalidate',
            name='size',
            field=models.CharField(choices=Learning_ORM_queries.models.LearnValidate.get_choices, default='Large', max_length=100),
            preserve_default=False,
        ),
    ]