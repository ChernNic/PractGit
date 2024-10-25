import django_filters
from dcim.models import Site  # Import the Site model
from netbox_plugin_buildingplan.models import BuildingPlan

class BuildingPlanFilter(django_filters.FilterSet):
    site = django_filters.ModelChoiceFilter(
        queryset=Site.objects.all(),  # Updated to use Site
        to_field_name="id",  # Using "id" for filtering by site ID
        label="Site",
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Plan Name",
    )

    class Meta:
        model = BuildingPlan
        fields = ['site', 'name']  # Updated fields to reflect site
