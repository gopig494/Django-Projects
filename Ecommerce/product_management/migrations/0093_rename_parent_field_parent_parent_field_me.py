# Generated by Django 5.0.4 on 2024-04-15 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0092_parent_2_alter_child_parent_link_child2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parent',
            old_name='parent_field',
            new_name='parent_field_me',
        ),
    ]
