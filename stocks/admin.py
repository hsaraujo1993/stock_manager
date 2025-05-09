from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from core.admin_actions import export_as_excel
from stocks.models import Stock


# Register your models here.


class LowStockFilter(SimpleListFilter):
    title = 'Estoque baixo'
    parameter_name = 'low_stock'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Abaixo de 3'),
            ('no', '3 ou mais'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(quantity__lt=3)
        elif value == 'no':
            return queryset.filter(quantity__gte=3)
        return queryset


# Admin de Estoque
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'product__category','low_stock_alert')
    search_fields = ('product__name', 'product__material_code')
    list_filter = (LowStockFilter, 'product__category')
    ordering = ('product__name',)
    actions = [export_as_excel]

    def low_stock_alert(self, obj):
        if 3 > obj.quantity > 0:
            return "⚠️ Estoque Baixo!"
        if obj.quantity == 0:
            return '🛑 Sem Estoque!'
        return "OK"

    low_stock_alert.short_description = 'Status Estoque'

    def product__category(self, obj):
        return obj.product.category

    product__category.short_description = 'Categoria'


