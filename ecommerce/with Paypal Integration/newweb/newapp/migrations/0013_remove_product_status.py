# Generated by Django 4.1.2 on 2022-11-14 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0012_remove_product_list_product_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
    ]
