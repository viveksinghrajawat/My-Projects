# Generated by Django 4.1.2 on 2022-10-17 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0003_alter_product_product_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_id',
            new_name='product_catagory',
        ),
    ]
