from django.apps import AppConfig


class SalesItemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_items'

    def ready(self):
        import sales_items.signals
