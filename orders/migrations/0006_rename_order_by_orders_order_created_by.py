# Generated by Django 5.0.7 on 2024-07-26 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderitem_items_orderitem_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='order_by',
            new_name='order_created_by',
        ),
    ]