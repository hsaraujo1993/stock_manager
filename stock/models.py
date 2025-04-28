import uuid
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome da Categoria')
    prefix = models.CharField(max_length=10, null=False, blank=False, verbose_name='Prefixo do Código')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

class Produto(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome do Produto')
    material_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='Código do Produto')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoria')
    description = models.TextField(blank=True, verbose_name='Descrição do Produto')
    status = models.BooleanField(default=False, verbose_name='Status de Produto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def save(self, *args, **kwargs):
        if not self.material_code:
            self.material_code = f"{self.category.prefix}-{str(uuid.uuid4())[:5]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material_code} - {self.name}"

class Stock(models.Model):
    product = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='stock', verbose_name='Produto')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"

class Price(models.Model):
    product = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='price', verbose_name='Produto')
    sale_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor de Revenda')
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor de Compra')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Preço'
        verbose_name_plural = 'Preços'

    def __str__(self):
        return f"{self.product.name} - R${self.sale_value:.2f}"

class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total', default=0)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def total(self):
        # Calcula o valor total da venda somando os subtotais dos itens
        return sum(item.subtotal() for item in self.items.all()) if self.pk else 0

    def save(self, *args, **kwargs):
        # Removemos a atualização automática do total_value aqui
        # para evitar problemas com objetos novos que não têm itens ainda
        super().save(*args, **kwargs)

    def __str__(self):
        if self.id is None or self.date is None:
            return "Venda não foi registrada."
        return f"Venda #{self.id} - {self.date.strftime('%d/%m/%Y %H:%M')}"

class SalesItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Venda')
    product = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='items', verbose_name='Produto')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Item Vendido'
        verbose_name_plural = 'Itens Vendidos'

    def subtotal(self):
        return self.product.price.sale_value * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

