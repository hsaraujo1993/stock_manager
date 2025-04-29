from django.contrib import admin

from categories.models import Category


# Register your models here.


# Admin de Categoria
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix')
    search_fields = ('name', 'prefix')  # Filtro por nome e prefixo
    list_filter = ('prefix',)  # Filtro por prefixo
