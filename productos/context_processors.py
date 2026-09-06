from pedidos.models import Pedido


def pedidos_pendientes(request):
    """Agrega el contador de pedidos pendientes a todas las plantillas."""
    if request.user.is_authenticated:
        total_pendientes = Pedido.objects.filter(estado='pendiente').count()
    else:
        total_pendientes = 0
    
    return {
        'total_pedidos_pendientes': total_pendientes,
    }