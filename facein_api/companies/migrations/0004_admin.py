# Generated by Django 2.2.12 on 2020-08-16 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_fix_name_field_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Room', 'verbose_name_plural': 'Rooms'},
        ),
        migrations.AlterField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Company is using FaceIn now', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(default='FaceIn', max_length=255, unique=True, verbose_name='Company name'),
        ),
        migrations.AlterField(
            model_name='room',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', related_query_name='room', to='companies.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='room',
            name='info',
            field=models.TextField(blank=True, max_length=1023, verbose_name='Additional notes'),
        ),
        migrations.AlterField(
            model_name='room',
            name='is_whitelisted',
            field=models.BooleanField(default=False, help_text='Only whitelist of people is allowed to enter the room, everybody except blacklist otherwise', verbose_name='Whitelist room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Room name'),
        ),
    ]
