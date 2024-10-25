import json
import os

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import RequestConfig
from django.db import transaction

from netbox import settings
from netbox.views import generic
from netbox_plugin_buildingplan.filtersets import BuildingPlanFilter
from netbox_plugin_buildingplan.tables import BuildingPlanTable
from dcim.models import Site, DeviceRole  # Import the Site model
from utilities.views import ViewTab, register_model_view
from netbox_plugin_buildingplan.models import BuildingPlan, BuildingPlanDevice, DeviceIcon
from netbox_plugin_buildingplan.forms import BuildingPlanForm, BuildingPlanAddForm, BuildingPlanFilterForm
from dcim.models import Device as DcimDevice



@register_model_view(Site, name="buildingplan_tab")
class BuildingPlanTabView(View):
    tab = ViewTab(
        label="Building Plan",
    )

    def get(self, request, pk):
        site = get_object_or_404(Site, pk=pk)  # Changed to Site
        building_plans = BuildingPlan.objects.filter(site=site)  # Filter by site
        table = BuildingPlanTable(data=building_plans)
        table.configure(request)

        return render(
            request,
            "netbox_plugin_buildingplan/building_plan_tab.html",
            context={
                "object": site,
                "table": table,
                "tab": self.tab,
            },
        )


class BuildingPlanCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "netbox_plugin_buildingplan.add_buildingplan"
    model = BuildingPlan
    form_class = BuildingPlanAddForm
    template_name = 'netbox_plugin_buildingplan/building_plan_add.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')


class BuildingPlanUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "netbox_plugin_buildingplan.change_buildingplan"
    model = BuildingPlan
    form_class = BuildingPlanForm
    template_name = "netbox_plugin_buildingplan/building_plan_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все устройства, связанные с сайтом плана здания
        site = self.object.site
        devices = DcimDevice.objects.filter(site=site).select_related('role')

        # Передаем устройства в контекст
        context['devices'] = devices

        return context

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')



class BuildingPlanDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "netbox_plugin_buildingplan.delete_buildingplan"
    model = BuildingPlan
    template_name = "netbox_plugin_buildingplan/building_plan_delete.html"

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')


class BuildingPlanListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = "netbox_plugin_buildingplan.view_buildingplan"
    model = BuildingPlan
    table = BuildingPlanTable
    template_name = 'netbox_plugin_buildingplan/building_plan_list.html'
    filterset = BuildingPlanFilter
    filterset_form = BuildingPlanFilterForm

    def dispatch(self, request, *args, **kwargs):
        queryset = BuildingPlan.objects.select_related('site').all()  # Updated to select related 'site'
        self.queryset = self.filterset(request.GET, queryset).qs
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset_form(self.request.GET)
        return context


class UpdateDevicesView(View):
    def post(self, request, pk):
        building_plan = get_object_or_404(BuildingPlan, pk=pk)
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                # Delete all old devices
                BuildingPlanDevice.objects.filter(building_plan=building_plan).delete()

                # Add new devices
                for device_data in data['devices']:
                    BuildingPlanDevice.objects.create(
                        building_plan=building_plan,
                        name=device_data['name'],
                        x_position=device_data['x_position'],
                        y_position=device_data['y_position'],
                        device_type=device_data['device_type']
                    )

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


class DeviceIconView(View):
    template_name = 'netbox_plugin_buildingplan/device_icon_view.html'

    def get(self, request, *args, **kwargs):
        # Получаем все иконки, сохраненные в базе данных
        icons_in_db = DeviceIcon.objects.all()

        # Получаем все файлы в папке static/icons/
        icons_directory = os.path.join(settings.STATIC_ROOT, 'icons')
        icons_in_filesystem = []
        if os.path.exists(icons_directory):
            icons_in_filesystem = [f for f in os.listdir(icons_directory) if os.path.isfile(os.path.join(icons_directory, f))]

        # Создаем список для хранения всех иконок, чтобы избежать дублирования
        all_icons = []

        # Добавляем иконки из базы данных в список all_icons
        for icon in icons_in_db:
            all_icons.append({
                'icon_path': icon.icon_path,
                'role': icon.role
            })

        # Добавляем иконки из файловой системы, которые еще не в базе данных
        for icon_file in icons_in_filesystem:
            if not icons_in_db.filter(icon_path=icon_file).exists():
                all_icons.append({
                    'icon_path': icon_file,
                    'role': None  # Не назначена никакая роль
                })

        # Определяем роли, которые еще не назначены иконкам
        assigned_roles = DeviceRole.objects.filter(icon__isnull=False)
        available_roles = DeviceRole.objects.exclude(id__in=assigned_roles.values_list('id', flat=True))

        return render(request, self.template_name, {
            'icons': all_icons,  # Список всех иконок, включая те, что в файловой системе
            'available_roles': available_roles,
        })



class AssignRoleView(View):
    def post(self, request):
        # Получаем данные из запроса
        role_id = request.POST.get('role')
        icon_path = request.POST.get('icon_path')

        # Проверяем наличие иконки в базе данных
        icon, created = DeviceIcon.objects.get_or_create(icon_path=icon_path)

        if role_id:
            # Если указана роль, назначаем её
            role = get_object_or_404(DeviceRole, id=role_id)

            # Проверяем, есть ли другая иконка с этой ролью, и отвязываем её
            DeviceIcon.objects.filter(role=role).update(role=None)

            # Назначаем роль текущей иконке
            icon.role = role
        else:
            # Если роль не указана, отвязываем текущую роль
            icon.role = None

        # Сохраняем изменения
        icon.save()

        # Перенаправляем обратно к списку иконок
        return redirect('plugins:netbox_plugin_buildingplan:device_icons')
