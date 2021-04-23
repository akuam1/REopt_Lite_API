# Generated by Django 2.2.13 on 2021-04-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reo', '0107_auto_20210420_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_from_elec_grid_purchase',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_from_elec_grid_purchase_bau',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_from_fuelburn',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_from_fuelburn_bau',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_offset_from_elec_exports',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitemodel',
            name='year_one_emissions_offset_from_elec_exports_bau',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
