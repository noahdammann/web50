# Generated by Django 4.1.1 on 2022-10-15 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_comment_listing_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
