from django.db import models

from products.models import Produto


# Create your models here.


class Stock(models.Model):
    product = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='stock', verbose_name='Produto')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"