from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    """
    Estructura preparada para registrar pedidos en el futuro.
    Por ahora los pedidos llegan por WhatsApp, pero la tabla
    queda lista para cuando quieras gestionarlos en el sistema.
    """

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Usuario que compro (puede estar vacio si compro por WhatsApp)'
    )
    producto_nombre = models.CharField(max_length=120)
    talla = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notificado = models.BooleanField(default=False)  # ← NUEVO: indica si ya viste este pedido
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.id} - {self.producto_nombre}'