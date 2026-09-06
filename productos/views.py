from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .models import Producto
from .forms import ProductoForm, CambiarPasswordForm
import urllib.parse
import csv
from django.http import HttpResponse

# =============================================
# VISTAS PÚBLICAS (TIENDA)
# =============================================

def inicio(request):
    """Pagina principal: muestra hasta 8 productos destacados."""
    productos = Producto.objects.filter(activo=True)[:8]
    return render(request, 'tienda/inicio.html', {
        'productos_destacados': productos,
    })


def lista_productos(request):
    """Catalogo completo: productos activos, con filtro, busqueda y ordenamiento."""
    from django.db.models import Q

    categoria_seleccionada = request.GET.get('categoria', '')
    busqueda = request.GET.get('q', '').strip()
    orden = request.GET.get('orden', 'recientes')

    # Empezar con todos los productos activos
    productos = Producto.objects.filter(activo=True)

    # Filtrar por categoría
    if categoria_seleccionada:
        productos = productos.filter(categoria=categoria_seleccionada)

    # Buscar por nombre o descripción
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )

    # Ordenar
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')
    else:  # 'recientes' por defecto
        productos = productos.order_by('-creado')

    # Lista de categorías para el menú de filtros
    categorias = Producto.CATEGORIAS

    return render(request, 'tienda/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_seleccionada,
        'busqueda': busqueda,
        'orden': orden,
    })


def detalle_producto(request, producto_id):
    """Pagina de detalle: informacion completa de una prenda."""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Productos relacionados de la misma categoría (excluyendo el actual)
    productos_relacionados = Producto.objects.filter(
        activo=True,
        categoria=producto.categoria
    ).exclude(id=producto.id)[:4]
    
    return render(request, 'tienda/detalle_producto.html', {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    })


def nosotros(request):
    """Pagina de informacion sobre la tienda."""
    return render(request, 'tienda/nosotros.html')


@require_POST  # Solo acepta peticiones POST (no GET)
def crear_pedido(request):
    """
    Recibe la seleccion del cliente (producto, talla, color, cantidad),
    valida en el servidor (no confia en el navegador),
    y devuelve la URL de WhatsApp con el mensaje listo.
    """
    from pedidos.models import Pedido

    producto_id = request.POST.get('producto_id')
    talla = request.POST.get('talla', '').strip()
    color = request.POST.get('color', '').strip()
    cantidad_str = request.POST.get('cantidad', '1')

    # ---------- VALIDACION 1: El producto existe y está activo ----------
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    # ---------- VALIDACION 2: La cantidad es un número válido ----------
    try:
        cantidad = int(cantidad_str)
        if cantidad < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Cantidad inválida.'}, status=400)

    # ---------- VALIDACION 3: La talla está en la lista del producto ----------
    tallas_validas = [t.strip().lower() for t in producto.tallas.split(',')]
    if talla.lower() not in tallas_validas:
        return JsonResponse({'error': 'Talla no válida para este producto.'}, status=400)

    # ---------- VALIDACION 4: El color está en la lista del producto ----------
    colores_validos = [c.strip().lower() for c in producto.colores.split(',')]
    if color.lower() not in colores_validos:
        return JsonResponse({'error': 'Color no válido para este producto.'}, status=400)

    # ---------- VALIDACION 5: Hay stock suficiente ----------
    if cantidad > producto.stock:
        return JsonResponse({'error': 'Stock insuficiente.'}, status=400)

    # ---------- VALIDACION 6: El producto no está agotado ----------
    if producto.agotado():
        return JsonResponse({'error': 'Producto agotado.'}, status=400)

    # ---------- REGISTRAR EL PEDIDO EN LA BASE DE DATOS ----------
    total = producto.precio * cantidad

    Pedido.objects.create(
        cliente=request.user if request.user.is_authenticated else None,
        producto_nombre=producto.nombre,
        talla=talla,
        color=color,
        cantidad=cantidad,
        precio_unitario=producto.precio,
        total=total,
        estado='pendiente',
    )

    # ---------- CONSTRUIR EL MENSAJE DE WHATSAPP ----------
    numero_whatsapp = settings.TIENDA_CONFIG['WHATSAPP_NUMERO']
    nombre_tienda = settings.TIENDA_CONFIG['NOMBRE_TIENDA']

    mensaje = (
        f"¡Hola {nombre_tienda}! 👋\n"
        f"Quiero comprar:\n"
        f"----------------\n"
        f"🛍️ Producto: {producto.nombre}\n"
        f"📏 Talla: {talla}\n"
        f"🎨 Color: {color}\n"
        f"🔢 Cantidad: {cantidad}\n"
        f"💰 Precio unitario: Bs. {producto.precio}\n"
        f"💵 TOTAL: Bs. {total}\n"
        f"----------------\n"
        f"¿Me confirmas la disponibilidad?"
    )

    # Codificar el mensaje para que funcione en una URL
    mensaje_codificado = urllib.parse.quote(mensaje)

    url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"

    return JsonResponse({'url': url_whatsapp})


# =============================================
# VISTAS DEL PANEL DE ADMINISTRACIÓN
# =============================================

def login_admin(request):
    """Pantalla de inicio de sesión del panel."""
    if request.user.is_authenticated:
        return redirect('panel_productos')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect('panel_productos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin_tienda/login.html', {'form': form})


def logout_admin(request):
    """Cerrar sesión."""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')


@login_required
def panel_productos(request):
    """Panel principal: estadísticas y lista de todos los productos."""
    from django.db.models import Sum
    from pedidos.models import Pedido

    # Estadísticas generales
    total_productos = Producto.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()
    productos_agotados = Producto.objects.filter(stock=0, activo=True).count()

    # Estadísticas de pedidos
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    pedidos_confirmados = Pedido.objects.filter(estado__in=['confirmado', 'preparando', 'enviado', 'entregado']).count()
    ingresos_totales = Pedido.objects.exclude(estado='cancelado').aggregate(total=Sum('total'))['total'] or 0

    # Productos más vendidos (por cantidad total)
    productos_mas_vendidos = Pedido.objects.exclude(estado='cancelado').values(
        'producto_nombre'
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]

    productos = Producto.objects.all()

    return render(request, 'admin_tienda/panel_productos.html', {
        'productos': productos,
        'total_productos': total_productos,
        'productos_activos': productos_activos,
        'productos_agotados': productos_agotados,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_confirmados': pedidos_confirmados,
        'ingresos_totales': ingresos_totales,
        'productos_mas_vendidos': productos_mas_vendidos,
    })


@login_required
def crear_producto(request):
    """Agregar un nuevo producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente.')
            return redirect('panel_productos')
    else:
        form = ProductoForm()

    return render(request, 'admin_tienda/formulario_producto.html', {
        'form': form,
        'titulo': 'Agregar producto',
        'boton': 'Guardar producto',
    })


@login_required
def editar_producto(request, producto_id):
    """Editar un producto existente."""
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('panel_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'admin_tienda/formulario_producto.html', {
        'form': form,
        'titulo': f'Editar: {producto.nombre}',
        'boton': 'Guardar cambios',
    })


@login_required
def eliminar_producto(request, producto_id):
    """Eliminar un producto."""
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
        return redirect('panel_productos')

    return render(request, 'admin_tienda/confirmar_eliminar.html', {
        'producto': producto,
    })


# =============================================
# VISTAS DE PEDIDOS
# =============================================

@login_required
def panel_pedidos(request):
    """Panel de pedidos: lista de todos los pedidos recibidos."""
    from pedidos.models import Pedido
    
    pedidos = Pedido.objects.all().order_by('-fecha')
    
    # Marcar todos los pedidos como notificados al verlos
    pedidos.filter(notificado=False).update(notificado=True)
    
    # Contar pedidos pendientes
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    
    return render(request, 'admin_tienda/panel_pedidos.html', {
        'pedidos': pedidos,
        'pedidos_pendientes': pedidos_pendientes,
    })


@login_required
def cambiar_estado_pedido(request, pedido_id):
    """Cambiar el estado de un pedido."""
    from pedidos.models import Pedido
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        estados_validos = ['pendiente', 'confirmado', 'preparando', 'enviado', 'entregado', 'cancelado']
        
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Pedido #{pedido.id} actualizado a "{pedido.get_estado_display()}".')
        else:
            messages.error(request, 'Estado no válido.')
    
    return redirect('panel_pedidos')


# =============================================
# VISTAS DE PERFIL
# =============================================

@login_required
def perfil_admin(request):
    """Página de perfil del administrador."""
    return render(request, 'admin_tienda/perfil.html', {
        'usuario': request.user,
    })


@login_required
def cambiar_password(request):
    """Cambiar la contraseña del administrador."""
    if request.method == 'POST':
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa
            messages.success(request, '¡Contraseña actualizada correctamente!')
            return redirect('perfil_admin')
        else:
            messages.error(request, 'No se pudo cambiar la contraseña. Verifica los datos.')
    else:
        form = CambiarPasswordForm(user=request.user)

    return render(request, 'admin_tienda/cambiar_password.html', {
        'form': form,
    })
@login_required
def exportar_pedidos_csv(request):
    """Exporta todos los pedidos a un archivo CSV para Excel."""
    from pedidos.models import Pedido

    pedidos = Pedido.objects.all().order_by('-fecha')

    # Crear la respuesta HTTP con tipo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
    response.write('\ufeff')  # BOM para que Excel detecte UTF-8

    writer = csv.writer(response)
    writer.writerow(['ID', 'Producto', 'Talla', 'Color', 'Cantidad', 
                     'Precio Unitario', 'Total', 'Estado', 'Fecha'])

    for pedido in pedidos:
        writer.writerow([
            pedido.id,
            pedido.producto_nombre,
            pedido.talla,
            pedido.color,
            pedido.cantidad,
            pedido.precio_unitario,
            pedido.total,
            pedido.get_estado_display(),
            pedido.fecha.strftime('%d/%m/%Y %H:%M'),
        ])

    return response