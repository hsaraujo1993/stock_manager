from django.contrib import admin, messages
from django.db.models import Sum

from core.admin_actions import export_as_excel
from sales.models import Sale
from sales_items.admin import SalesItemInline

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SalesItemInline]
    readonly_fields = ('date', 'total_value')
    search_fields = ('date', 'total_value', 'id')
    list_filter = ('date',)
    list_display = ('id_display', 'date', 'total_value_display',)
    actions = [export_as_excel]

    def total_value_display(self, obj):
        return f"R${obj.total_value:.2f}"
    total_value_display.short_description = 'Valor Total'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            cl = self.get_changelist_instance(request)
            queryset = cl.get_queryset(request)

            total_sales_value = queryset.aggregate(total=Sum('total_value'))['total'] or 0

            messages.info(
                request,
                f"Valor total das vendas filtradas: R${total_sales_value:.2f}"
            )
        except Exception as e:
            messages.warning(request, f"Erro ao calcular o total filtrado: {str(e)}")

        return response

    def get_form(self, request, obj=None, **kwargs):
        self.current_request = request
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        if not formset.is_valid():
            return

        instances = formset.save(commit=False)

        if not instances and not change:
            messages.error(request, "Uma venda deve ter pelo menos um item.")
            return

        has_error = False
        for instance in instances:
            if not instance.id:
                stock = instance.product.stock
                if stock.quantity < instance.quantity:
                    messages.error(
                        request,
                        f"Estoque insuficiente para {instance.product.name}. " +
                        f"Disponível: {stock.quantity}, Solicitado: {instance.quantity}"
                    )
                    has_error = True

        if has_error:
            return

        if not change:
            super().save_model(request, form.instance, form, change)

        for instance in instances:
            stock = instance.product.stock
            stock.quantity -= instance.quantity
            stock.save()
            instance.save()

        formset.save_m2m()

        sale = form.instance
        sale.total_value = sum(item.subtotal() for item in sale.items.all())
        sale.save(update_fields=['total_value'])

    def id_display(self, obj):
        return f"Pedido #{obj.id}"

    id_display.short_description = 'Pedido'
