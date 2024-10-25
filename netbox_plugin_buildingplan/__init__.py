from netbox.plugins import PluginConfig
from .version import __version__

class BuildingPLanConfig(PluginConfig):
    name = "netbox_plugin_buildingplan"
    verbose_name = "Buildingplan"
    description = "An example NetBox plugin"
    version = __version__
    author = "Ledy Gaga"
    base_url = "buildingplan"
    required_settings = []
    default_settings = {}

config = BuildingPLanConfig
