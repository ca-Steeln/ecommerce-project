# Generated by Django 4.2 on 2023-11-17 01:51

import accounts.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=13, region='DZ')),
                ('image', models.ImageField(blank=True, default=accounts.models.Account.default_directory_path, upload_to=accounts.models.Account.directory_path)),
            ],
        ),
    ]
