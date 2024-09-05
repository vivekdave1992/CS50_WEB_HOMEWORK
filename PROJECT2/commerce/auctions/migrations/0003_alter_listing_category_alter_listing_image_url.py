# Generated by Django 5.1 on 2024-09-05 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_catagory_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_catagory', to='auctions.catagory'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
