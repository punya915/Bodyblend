# Generated by Django 4.2.6 on 2023-10-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_dresscolour_dress_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dress',
            name='gender',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
