from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_plugin_buildingplan.models import BuildingPlan

class BuildingPlanSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_plugin_buildingplan-api:buildingplan-detail'
    )

    class Meta:
        model = BuildingPlan
        fields = ('id', 'name', 'site', 'image', 'url')