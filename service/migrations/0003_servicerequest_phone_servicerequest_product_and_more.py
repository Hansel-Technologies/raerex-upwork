# Generated by Django 5.0.6 on 2024-08-02 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_equipmentcategory_remove_servicerequest_status_and_more'),
        ('shop', '0009_product_catalogue_product_requires_installation'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='email',
            field=models.EmailField(default='unknown@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='location',
            field=models.CharField(default='Unspecified', max_length=255),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='name',
            field=models.CharField(default='Unknown Customer', max_length=100),
        ),
    ]
