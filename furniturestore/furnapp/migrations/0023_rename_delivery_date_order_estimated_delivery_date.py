# Generated by Django 5.0.1 on 2024-02-12 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('furnapp', '0022_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivery_date',
            new_name='Estimated_delivery_date',
        ),
    ]