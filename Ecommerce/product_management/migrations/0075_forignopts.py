# Generated by Django 5.0.4 on 2024-04-14 09:29

import django.db.models.deletion
import product_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0074_remove_fieldtypescheckl2_json_ob'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForignOpts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b', models.ForeignKey(limit_choices_to={'author': 'Gopi'}, on_delete=django.db.models.deletion.DO_NOTHING, to='product_management.book')),
                ('dis', models.ForeignKey(default='unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='product_management.discount')),
                ('dis_info', models.ForeignKey(on_delete=models.SET(product_management.models.set_def), to='product_management.discountinfo')),
                ('filed_c2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_management.fieldtypescheckl2')),
                ('filed_c3', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='product_management.fieldcheck3')),
                ('filed_l', models.ForeignKey(default='unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='product_management.fieldtypescheckl')),
                ('product_forign', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_management.checkuuid')),
                ('se_itm', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product_management.stockentry')),
            ],
        ),
    ]
