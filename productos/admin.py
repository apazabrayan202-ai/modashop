from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista de productos
    list_display = ('nombre', 'precio', 'categoria', 'stock', 'activo', 'creado')
    # Barra lateral con filtros
    list_filter = ('categoria', 'activo')
    # Campo de busqueda
    search_fields = ('nombre', 'descripcion')
    # Orden de los campos en el formulario de edicion
    fields = ('nombre', 'descripcion', 'precio', 'imagen', 'categoria',
              'tallas', 'colores', 'stock', 'activo')