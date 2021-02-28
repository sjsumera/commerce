# Generated by Django 3.1.7 on 2021-02-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
