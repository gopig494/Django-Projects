# Generated by Django 5.0.4 on 2024-04-14 15:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0076_alter_forignopts_b_alter_forignopts_dis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forignopts',
            name='b',
            field=models.ForeignKey(limit_choices_to={'author': 1}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product_management.book'),
        ),
    ]
