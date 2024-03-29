# Generated by Django 5.0.1 on 2024-02-13 15:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furnapp', '0023_rename_delivery_date_order_estimated_delivery_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileimage', models.ImageField(null=True, upload_to='brandlogo')),
                ('fullname', models.CharField(max_length=100, null=True)),
                ('contact', models.BigIntegerField(null=True)),
                ('permanantaddress', models.CharField(max_length=300, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
