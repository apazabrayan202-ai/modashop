from django.urls import path
from . import views

urlpatterns = [
    # Rutas públicas (tienda)
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('pedido/', views.crear_pedido, name='crear_pedido'),
    path('nosotros/', views.nosotros, name='nosotros'),

    # Rutas del panel de administración
    path('panel/login/', views.login_admin, name='login'),
    path('panel/logout/', views.logout_admin, name='logout'),
    path('panel/', views.panel_productos, name='panel_productos'),
    path('panel/crear/', views.crear_producto, name='crear_producto'),
    path('panel/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('panel/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('panel/pedidos/', views.panel_pedidos, name='panel_pedidos'),
    path('panel/pedido/<int:pedido_id>/estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('panel/perfil/', views.perfil_admin, name='perfil_admin'),  # ← NUEVA
    path('panel/cambiar-password/', views.cambiar_password, name='cambiar_password'),  # ← NUEVA
path('panel/exportar-pedidos/', views.exportar_pedidos_csv, name='exportar_pedidos'),
]