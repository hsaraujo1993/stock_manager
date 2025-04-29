from django.contrib import admin, messages
from django.db.models import Sum

from prices.models import Price


# Register your models here.

# Admin de Preço
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'formatted_sale_value', 'formatted_purchase_value')
    search_fields = ('product__name',)
    list_filter = ('product__category',)
    ordering = ('product__name',)

    def formatted_sale_value(self, obj):
        return f"R${obj.sale_value:.2f}"

    def formatted_purchase_value(self, obj):
        return f"R${obj.purchase_value:.2f}"

    formatted_sale_value.admin_order_field = 'sale_value'
    formatted_purchase_value.admin_order_field = 'purchase_value'

    formatted_sale_value.short_description = 'Preço de Revenda'
    formatted_purchase_value.short_description = 'Preço de Compra'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            qs = response.context_data['cl'].queryset

            total_sale = qs.aggregate(total_sale=Sum('sale_value'))['total_sale'] or 0
            total_purchase = qs.aggregate(total_purchase=Sum('purchase_value'))['total_purchase'] or 0

            messages.info(
                request,
                f"Valor Investido: R${total_purchase:.2f}    -    Valor a Receber após as Vendas (incluindo Lucro): R${total_sale:.2f}"
            )

        return response
