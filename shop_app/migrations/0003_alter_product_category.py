# Generated by Django 5.1.2 on 2024-10-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Asus', 'ASUS'), ('Hp', 'HP'), ('Dell', 'DELL'), ('Macbook', 'MACBOOK')], max_length=15, null=True),
        ),
    ]
