from django.urls import path
from .views import *

urlpatterns = [
    path('sites/<int:pk>/building-plan/', BuildingPlanTabView.as_view(), name='buildingplan_tab'),
    path('building-plan_page/', BuildingPlanListView.as_view(), name='buildingplan_list'),
    path('building-plan/add/', BuildingPlanCreateView.as_view(), name='buildingplan_add'),
    path('building-plan/<int:pk>/edit/', BuildingPlanUpdateView.as_view(), name='buildingplan_edit'),
    path('building-plan/<int:pk>/delete/', BuildingPlanDeleteView.as_view(), name='buildingplan_delete'),
    path('building-plan/<int:pk>/update-devices/', UpdateDevicesView.as_view(), name='update_devices'),

    path('device-icons/', DeviceIconView.as_view(), name='device_icons'),
    path('device-icons/assign-role/', AssignRoleView.as_view(), name='assign_role'),
]
