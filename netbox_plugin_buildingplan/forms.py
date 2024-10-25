from django import forms
from dcim.models import Site  # Import Site model
from netbox.forms import NetBoxModelFilterSetForm
from .models import BuildingPlan, BuildingPlanDevice


class BuildingPlanForm(forms.ModelForm):
    class Meta:
        model = BuildingPlan
        fields = ['name', 'image']


class BuildingPlanAddForm(forms.ModelForm):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), label='Site')  # Changed from Tenant to Site
    name = forms.CharField(label='Plan Name')
    image = forms.ImageField(label='Building Plan Image')

    class Meta:
        model = BuildingPlan
        fields = ['site', 'name', 'image']  # Changed tenant to site


class BuildingPlanFilterForm(forms.ModelForm):
    site = forms.ModelChoiceField(queryset=Site.objects.all(), required=False, label="Site")  # Changed from Tenant to Site
    name = forms.CharField(required=False, label="Plan Name")

    class Meta:
        model = BuildingPlan
        fields = ['site', 'name']  # Changed tenant to site

