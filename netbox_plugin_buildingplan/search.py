from netbox.search import SearchIndex, register_search
from .models import BuildingPlan

@register_search
class BuildingPlanIndex(SearchIndex):
    model = BuildingPlan
    fields = (
        ('name', 100),
    )

