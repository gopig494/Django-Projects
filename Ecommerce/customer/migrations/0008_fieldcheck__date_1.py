# Generated by Django 5.0.4 on 2024-04-06 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_fieldcheck__date_alter_fieldcheck__db_col_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldcheck',
            name='_date_1',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]