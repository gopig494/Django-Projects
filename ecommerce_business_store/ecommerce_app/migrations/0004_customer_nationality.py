# Generated by Django 4.2.5 on 2023-09-20 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0003_nationality_alter_customeraddress_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='nationality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecommerce_app.nationality'),
            preserve_default=False,
        ),
    ]
