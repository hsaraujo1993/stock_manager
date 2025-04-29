import uuid

from django.db import models

from categories.models import Category


# Create your models here.


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
            self.material_code = f"{self.category.prefix}-{str(uuid.uuid4())[:5].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material_code} - {self.name}"
