from django.contrib import admin
from django import forms

from products.models import Produto
from sales_items.models import SalesItem


# Register your models here.


class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SalesItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra produtos com status ativo, com preço e com estoque
        self.fields['product'].queryset = Produto.objects.filter(
            status=True,  # Produtos ativos
            price__isnull=False,  # Produtos com preço
            stock__quantity__gt=0  # Produtos com estoque
        )


# Inline dos Itens de Venda
class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0  # Melhor deixar 0 para não ficar aparecendo linha vazia
    fields = ('product', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)
    form = SalesItemForm  # Usando o formulário customizado

    def subtotal(self, obj):
        if not obj.id:  # Se o objeto ainda não existe
            return "Calcular após salvar"
        return f"R${obj.product.price.sale_value * obj.quantity:.2f}"

    subtotal.short_description = 'Subtotal'

    def get_queryset(self, request):
        # Filtra apenas produtos com status ativo, preço e estoque
        queryset = super().get_queryset(request)
        return queryset.filter(
            product__status=True,  # Só exibe produtos ativos
            product__price__isnull=False,  # Com preço
            product__stock__quantity__gt=0  # Com estoque disponível
        )


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'subtotal_display')
    search_fields = ('product__name',)  # Filtro por nome do produto
    list_filter = ('product__category',)  # Filtro por categoria do produto

    def subtotal_display(self, obj):
        return f"R${obj.subtotal():.2f}"

    subtotal_display.short_description = 'Subtotal'