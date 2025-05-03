from django.contrib import admin
from django import forms

from core.admin_actions import export_as_excel
from products.models import Produto
from sales_items.models import SalesItem


# Register your models here.


class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SalesItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].queryset = Produto.objects.filter(
            status=True,
            price__isnull=False,
            stock__quantity__gt=0
        )


# Inline dos Itens de Venda
class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0
    fields = ('product', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)
    form = SalesItemForm

    def subtotal(self, obj):
        if not obj.id:
            return "Calcular após salvar"
        return f"R${obj.product.price.sale_value * obj.quantity:.2f}"

    subtotal.short_description = 'Subtotal'

    def get_queryset(self, request):

        queryset = super().get_queryset(request)
        return queryset.filter(
            product__status=True,
            product__price__isnull=False,
            product__stock__quantity__gt=0
        )


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = ('sale_id_display', 'sale__date', 'product', 'quantity', 'subtotal_display')
    list_filter = ('product__category', 'sale__id', 'sale__date')
    actions = [export_as_excel]

    def subtotal_display(self, obj):
        return f"R${obj.subtotal():.2f}"

    subtotal_display.short_description = 'Subtotal'

    def sale_id_display(self, obj):
        return f"Pedido #{obj.sale.id}"

    sale_id_display.short_description = 'Pedidos'

    def sale__date(self, obj):
        return obj.sale.date
    sale__date.short_description = 'Data'
