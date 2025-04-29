from django.db import models

from products.models import Produto


# Create your models here.


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