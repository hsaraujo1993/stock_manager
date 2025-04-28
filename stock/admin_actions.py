import openpyxl
from django.http import HttpResponse
from django.utils.timezone import localtime

def export_as_excel(modeladmin, request, queryset):
    # Pega todos os registros da tabela
    queryset = modeladmin.model.objects.all()

    # Verifica se há registros para exportar
    if not queryset.exists():
        modeladmin.message_user(request, "Não há registros para exportar.", level='warning')
        return HttpResponse("Não há registros para exportar.")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = modeladmin.model._meta.verbose_name_plural.title()

    fields = [field.name for field in modeladmin.model._meta.fields]

    ws.append(fields)

    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field)
            if callable(value):
                value = value()
            if isinstance(value, bool):
                value = "Sim" if value else "Não"
            if hasattr(value, 'strftime'):
                value = localtime(value).strftime('%d/%m/%Y %H:%M')
            row.append(str(value))
        ws.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta.model_name}s.xlsx'
    wb.save(response)
    return response

export_as_excel.short_description = "Exportar todos para Excel"
