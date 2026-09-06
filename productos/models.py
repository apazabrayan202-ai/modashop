from django.db import models
from django.core.validators import MinValueValidator


class Producto(models.Model):
    """
    Representa una prenda de ropa en la tienda.
    Cada campo de esta clase sera una columna en la tabla de la base de datos.
    """

    # --- Datos basicos ---
    nombre = models.CharField(
        max_length=120,
        help_text='Ej: Camiseta Oversize'
    )
    descripcion = models.TextField(
        help_text='Descripcion detallada de la prenda'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],  # El precio nunca puede ser negativo
        help_text='Precio en bolivianos (Bs)'
    )

    # --- Imagen ---
    # Las fotos se guardaran en media/productos/
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,      # Permite guardar sin imagen (por si acaso)
        null=True,
        help_text='Foto de la prenda'
    )

    # --- Clasificacion ---
    CATEGORIAS = [
        ('mujer', 'Mujer'),
        ('hombre', 'Hombre'),
        ('ninos', 'Ninos'),
        ('calzado', 'Calzado'),
        ('accesorios', 'Accesorios'),
        ('abrigos', 'Abrigos'),
    ]
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='mujer'
    )

    # --- Tallas y colores ---
    # Separados por comas. Ej: "M, L, XL" o "30, 32, 34" para jeans
    tallas = models.CharField(
        max_length=200,
        help_text='Separadas por comas. Ej: M, L, XL'
    )
    colores = models.CharField(
        max_length=200,
        help_text='Separados por comas. Ej: Negro, Blanco'
    )

    # --- Inventario ---
    stock = models.PositiveIntegerField(
        default=0,
        help_text='Cantidad disponible. 0 = AGOTADO'
    )

    # --- Control ---
    activo = models.BooleanField(
        default=True,
        help_text='Desactivar oculta el producto de la tienda sin borrarlo'
    )
    creado = models.DateTimeField(auto_now_add=True)      # Fecha de creacion (automatica)
    actualizado = models.DateTimeField(auto_now=True)     # Se actualiza solo en cada cambio

    class Meta:
        ordering = ['-creado']   # Los productos nuevos aparecen primero
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        # Asi se muestra el producto en el panel y en la consola
        return self.nombre

    def agotado(self):
        # True cuando no hay stock. La usaremos para mostrar "AGOTADO"
        return self.stock <= 0