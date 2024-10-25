# Generated by Django 5.0.8 on 2024-09-18 20:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_plugin_buildingplan', '0003_buildingplan_created_buildingplan_custom_field_data_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingPlanDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('x_position', models.FloatField()),
                ('y_position', models.FloatField()),
                ('device_type', models.CharField(max_length=50)),
                ('building_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='netbox_plugin_buildingplan.buildingplan')),
            ],
        ),
    ]
