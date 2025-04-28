# admin.py
from django.contrib import admin, messages
from django.db.models import Sum
from .admin_actions import export_as_excel
from .models import Category, Produto, Stock, Price, Sale, SalesItem


# Admin de Categoria
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix')
    search_fields = ('name', 'prefix')  # Filtro por nome e prefixo
    list_filter = ('prefix',)  # Filtro por prefixo


# Admin de Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'material_code', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'material_code')
    list_filter = ('category', 'status', 'created_at')  # Filtro por categoria, status e data de criação
    ordering = ('name',)


# Admin de Estoque
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)  # Filtro por nome do produto
    list_filter = ('product__category',)  # Filtro por categoria do produto
    ordering = ('product__name',)
    actions = [export_as_excel]


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

    # >>>>>> AQUI você adiciona o changelist_view:


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


# Inline dos Itens de Venda
class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0  # Melhor deixar 0 para não ficar aparecendo linha vazia
    fields = ('product', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)
    can_delete = True  # Deixa deletar depois de salvar também
    show_change_link = True  # Opcional: vira link para editar o item se quiser

    def subtotal(self, obj):
        if not obj.id:  # Se o objeto ainda não existe
            return "Calcular após salvar"
        return f"R${obj.product.price.sale_value * obj.quantity:.2f}"

    subtotal.short_description = 'Subtotal'


# Admin da Venda
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SalesItemInline]
    readonly_fields = ('date', 'total_value')
    search_fields = ('date', 'total_value', 'id')
    list_filter = ('date',)
    list_display = ('id', 'date', 'total_value_display',)

    class Media:
        js = ('admin/js/keep_tab.js',)

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
            if not instance.id:  # Somente para novos itens
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

    def total_value_display(self, obj):
        return f"R${obj.total_value:.2f}"

    total_value_display.short_description = 'Valor Total'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            qs = response.context_data['cl'].queryset

            # Somando o valor total das vendas
            total_sale = qs.aggregate(total_sale=Sum('total_value'))['total_sale'] or 0

            # Exibindo as somas no topo da página
            messages.info(
                request,
                f"Valor Total das Vendas: R${total_sale:.2f}"
            )

        return response


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'subtotal_display')
    search_fields = ('product__name',)  # Filtro por nome do produto
    list_filter = ('product__category',)  # Filtro por categoria do produto

    def subtotal_display(self, obj):
        return f"R${obj.subtotal():.2f}"

    subtotal_display.short_description = 'Subtotal'
