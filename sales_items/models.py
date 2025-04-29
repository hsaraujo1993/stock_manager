from django.db import models

from products.models import Produto
from sales.models import Sale


# Create your models here.


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