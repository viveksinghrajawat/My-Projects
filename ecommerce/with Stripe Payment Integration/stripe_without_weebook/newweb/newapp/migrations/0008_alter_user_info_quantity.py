# Generated by Django 4.1.1 on 2022-10-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0007_user_info_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
