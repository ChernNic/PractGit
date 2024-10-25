from pathlib import Path
from django.contrib.sessions.backends import file
from setuptools import find_packages, setup

PACKAGE_NAME = "netbox_plugin_buildingplan"

setup(
    name=PACKAGE_NAME,
    version= "0.1",
    description="A NetBox plugin to add building plans to tenants.",
    author="Ledy Gaga",
    license="MIT",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)