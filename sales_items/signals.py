from django.db.models.signals import pre_delete
from django.dispatch import receiver

from sales_items.models import SalesItem


@receiver(pre_delete, sender=SalesItem)
def return_stock_on_delete(sender, instance, **kwargs):
    product = instance.product

    # Retorna a quantidade ao estoque
    if product.stock:
        product.stock.quantity += instance.quantity
        product.stock.save()
