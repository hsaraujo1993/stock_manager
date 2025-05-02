from django.db import models
from django.apps import AppConfig
from decimal import Decimal


# Create your models here.

class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total', default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        if self.id is None or self.date is None:
            return "Venda não foi registrada."
        return f"Venda #{self.id} - {self.date.strftime('%d/%m/%Y %H:%M')}"

    @property
    def total(self):
        # Calcula o valor total da venda somando os subtotais dos itens
        return sum(item.subtotal() for item in self.items.all()) if self.pk else Decimal('0.00')

    def save(self, *args, **kwargs):
        # Atualiza o campo total_value automaticamente ao salvar a venda
        self.total_value = self.total  # Atribui o valor calculado de `total` ao campo `total_value`
        super().save(*args, **kwargs)


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'
    verbose_name = 'Vendas'
