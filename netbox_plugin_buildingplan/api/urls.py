from netbox.api.routers import NetBoxRouter
from .views import BuildingPlanViewSet

router = NetBoxRouter()
router.register('buildingplan', BuildingPlanViewSet)

urlpatterns = router.urls
