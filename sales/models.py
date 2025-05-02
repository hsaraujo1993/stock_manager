from django.db import models
from django.apps import AppConfig


# Create your models here.

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

    @property
    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'
    verbose_name = 'Vendas'
