# Generated by Django 2.2.6 on 2019-10-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0002_auto_20191012_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='IdPhotoNegative',
            field=models.ImageField(height_field=100, max_length=400, null=True, upload_to='', width_field=100),
        ),
        migrations.AlterField(
            model_name='certification',
            name='IdPhotoPositive',
            field=models.ImageField(height_field=100, max_length=400, null=True, upload_to='', width_field=100),
        ),
    ]
