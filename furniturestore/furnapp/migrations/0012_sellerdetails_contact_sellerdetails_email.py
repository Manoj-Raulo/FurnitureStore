# Generated by Django 5.0.1 on 2024-02-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furnapp', '0011_sellerdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerdetails',
            name='contact',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sellerdetails',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
