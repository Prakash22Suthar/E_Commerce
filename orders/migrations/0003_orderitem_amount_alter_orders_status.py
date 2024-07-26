# Generated by Django 5.0.7 on 2024-07-26 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=50),
        ),
    ]
