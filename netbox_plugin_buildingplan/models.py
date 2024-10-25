from django.db import models
from django.urls import reverse
from dcim.models import Site
from netbox.models import NetBoxModel
from dcim.models.devices import DeviceRole

class BuildingPlan(NetBoxModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="building_plans")  # Use site instead of tenant
    name = models.CharField(max_length=255, verbose_name="Plan Name")
    image = models.ImageField(upload_to='building_plans/')

    def __str__(self):
        return f"Building Plan for {self.site.name}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_edit', kwargs={'pk': self.pk})


class BuildingPlanDevice(models.Model):
    building_plan = models.ForeignKey(BuildingPlan, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=255)
    x_position = models.FloatField()
    y_position = models.FloatField()
    icon = models.ImageField( null=True, blank=True)

    def __str__(self):
        return f"{self.name} on {self.building_plan.name}"

class DeviceIcon(models.Model):
    role = models.OneToOneField(DeviceRole, on_delete=models.CASCADE, related_name='icon', null=True, blank=True)
    icon_path = models.CharField(max_length=255, verbose_name="Device Icon Path")

    def __str__(self):
        return f"Icon for {self.role.name}"
