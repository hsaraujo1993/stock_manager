from django.contrib import admin

from products.models import Produto


# Register your models here.


# Admin de Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'material_code', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'material_code')
    list_filter = ('category', 'status', 'created_at')  # Filtro por categoria, status e data de criação
    ordering = ('name',)
    exclude = ('material_code',)
