# Generated by Django 4.1.2 on 2022-10-27 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0009_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.CharField(max_length=120),
        ),
    ]
