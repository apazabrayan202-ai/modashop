from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Configuración del panel de pedidos."""
    
    # Columnas que se ven en la lista
    list_display = ('id', 'producto_nombre', 'talla', 'color', 'cantidad', 
                    'total', 'estado', 'fecha')
    
    # Filtros laterales
    list_filter = ('estado', 'fecha', 'talla')
    
    # Búsqueda
    search_fields = ('producto_nombre', 'color')
    
    # Solo lectura (los pedidos se crean desde la tienda, no se editan manualmente)
    readonly_fields = ('producto_nombre', 'talla', 'color', 'cantidad', 
                       'precio_unitario', 'total', 'fecha')
    
    # Orden por defecto
    ordering = ('-fecha',)