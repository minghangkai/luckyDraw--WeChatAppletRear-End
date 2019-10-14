# Generated by Django 2.2.6 on 2019-10-14 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0004_auto_20191012_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='check',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='certification',
            name='IdPhotoNegative',
            field=models.ImageField(max_length=400, null=True, upload_to='uploadfile/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='IdPhotoPositive',
            field=models.ImageField(max_length=400, null=True, upload_to='uploadfile/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='OrganizationIdPhoto',
            field=models.ImageField(max_length=400, null=True, upload_to='uploadfile/%Y/%m/%d/'),
        ),
    ]
