# Generated by Django 3.1.7 on 2021-04-27 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reo', '0110_auto_20210323_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatormodel',
            name='useful_life_years',
            field=models.FloatField(blank=True, null=True),
        ),
    ]