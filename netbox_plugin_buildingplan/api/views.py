from netbox.api.viewsets import NetBoxModelViewSet
from netbox_plugin_buildingplan.models import BuildingPlan
from .serializers import BuildingPlanSerializer

class BuildingPlanViewSet(NetBoxModelViewSet):
    queryset = BuildingPlan.objects.all()
    serializer_class = BuildingPlanSerializer
