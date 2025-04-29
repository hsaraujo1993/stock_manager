from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome da Categoria')
    prefix = models.CharField(max_length=10, null=False, blank=False, verbose_name='Prefixo do Código')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name
