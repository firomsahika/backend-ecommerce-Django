# Generated by Django 4.2.16 on 2024-11-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0005_chapatransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Laptop', 'LAPTOP'), ('Headset', 'HEADSET'), ('Speaker', 'SPEAKER'), ('Mobile', 'MOBILE'), ('Watch', 'WATCH')], max_length=15, null=True),
        ),
    ]