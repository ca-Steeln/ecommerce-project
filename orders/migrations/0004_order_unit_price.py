# Generated by Django 4.2 on 2023-10-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_client_alter_order_order_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unit_price',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
    ]
