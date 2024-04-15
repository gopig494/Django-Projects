# Generated by Django 5.0.4 on 2024-04-15 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0089_alter_user_1_following'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Membership_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('invite_reason', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.group_1')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.person_1')),
            ],
        ),
        migrations.AddField(
            model_name='group_1',
            name='members',
            field=models.ManyToManyField(through='product_management.Membership_1', to='product_management.person_1'),
        ),
    ]
