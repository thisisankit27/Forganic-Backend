# Generated by Django 4.2.4 on 2023-10-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0002_cartitem_delivery_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_payment_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
