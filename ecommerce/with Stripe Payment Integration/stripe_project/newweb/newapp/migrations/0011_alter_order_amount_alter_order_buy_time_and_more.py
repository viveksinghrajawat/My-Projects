# Generated by Django 4.1.2 on 2022-10-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0010_rename_description_order_order_id_remove_order_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='buy_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_satuts',
            field=models.CharField(max_length=120),
        ),
    ]
