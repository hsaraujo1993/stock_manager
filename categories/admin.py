from django.contrib import admin

from core.admin_actions import export_as_excel
from categories.models import Category


# Register your models here.


# Admin de Categoria
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'created_at')
    search_fields = ('name', 'prefix')  # Filtro por nome e prefixo
    list_filter = ('prefix',)  # Filtro por prefixo
    actions = [export_as_excel]
