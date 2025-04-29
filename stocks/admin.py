from django.contrib import admin

from stocks.admin_actions import export_as_excel
from stocks.models import Stock


# Register your models here.

# Admin de Estoque
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)  # Filtro por nome do produto
    list_filter = ('product__category',)  # Filtro por categoria do produto
    ordering = ('product__name',)
    actions = [export_as_excel]
