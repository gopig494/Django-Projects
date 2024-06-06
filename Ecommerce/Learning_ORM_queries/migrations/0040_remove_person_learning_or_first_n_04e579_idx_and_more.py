# Generated by Django 5.0.4 on 2024-05-31 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0039_alter_learnmanaged_options_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='person',
            name='Learning_OR_first_n_04e579_idx',
        ),
        migrations.RemoveIndex(
            model_name='person',
            name='first_name_indexing',
        ),
        migrations.RemoveIndex(
            model_name='person',
            name='first_name_last_name_indexing',
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.CheckConstraint(check=models.Q(('first_name__startswith', 'g')), name='check_first_name_constraint'),
        ),
    ]