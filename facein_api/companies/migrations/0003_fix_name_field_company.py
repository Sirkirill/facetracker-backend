# Generated by Django 2.2.12 on 2020-05-24 20:52

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('companies', '0002_add_main_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(default='FaceIn', max_length=255, unique=True,
                                   verbose_name='Компания'),
        ),
    ]
