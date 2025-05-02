from django.db.models.signals import pre_delete, post_save, post_delete
from django.dispatch import receiver
from sales_items.models import SalesItem


@receiver(pre_delete, sender=SalesItem)
def return_stock_on_delete(sender, instance, **kwargs):
    product = instance.product

    # Retorna a quantidade ao estoque
    if product.stock:
        product.stock.quantity += instance.quantity
        product.stock.save()


@receiver(post_save, sender=SalesItem)
@receiver(post_delete, sender=SalesItem)
def update_sale_total(sender, instance, **kwargs):
    """
    Atualiza o total da venda sempre que um SalesItem for alterado ou deletado.
    """
    sale = instance.sale
    sale.total_value = sum(item.subtotal() for item in sale.items.all())  # Recalcula o total
    sale.save()  # Salva a venda com o novo total
