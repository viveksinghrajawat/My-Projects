# Generated by Django 4.1.2 on 2022-11-14 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0013_remove_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='temp',
            field=models.CharField(default='', max_length=450),
        ),
    ]
