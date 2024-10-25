import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import BuildingPlan
from netbox.tables import columns

class BuildingPlanTable(NetBoxTable):
    name = tables.TemplateColumn(
        template_code=(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#imageModal{{ record.id }}">{{ record.name }}</a>'
            '<div class="modal fade" id="imageModal{{ record.id }}" tabindex="-1" aria-labelledby="imageModalLabel{{ record.id }}" aria-hidden="true">'
            '  <div class="modal-dialog modal-lg">'
            '    <div class="modal-content">'
            '      <div class="modal-header">'
            '        <h5 class="modal-title" id="imageModalLabel{{ record.id }}">{{ record.name }}</h5>'
            '        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
            '      </div>'
            '      <div class="modal-body">'
            '        <img src="{{ record.image.url }}" alt="{{ record.name }}" class="img-fluid">'
            '      </div>'
            '      <div class="modal-footer">'
            '        <a href="{{ record.image.url }}" type="button" class="btn btn-secondary">Open</a>'
            '      </div>'
            '    </div>'
            '  </div>'
            '</div>'
        ),
        verbose_name='Plan Name'
    )
    site_name = tables.Column(accessor='site.name', verbose_name='Site Name')  # Updated to use site
    site_group = tables.Column(accessor='site.group.name', verbose_name='Site Group')  # Updated to use site group
    description = tables.Column(accessor='site.description', verbose_name='Description')  # Assuming site has a description field

    actions = columns.ActionsColumn(
        actions=('edit', 'delete'),
    )

    class Meta(NetBoxTable.Meta):
        model = BuildingPlan
        fields = ('name', 'site_name', 'site_group', 'description')
        default_columns = ('name', 'site_name', 'site_group', 'description')
