# Generated by Django 3.1.12 on 2021-08-16 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reo', '0105_auto_20210805_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemodel',
            name='desired_energy_burden_threshold_bau_percent',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
