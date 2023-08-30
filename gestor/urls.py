from django.urls import path
from .views import create_factura, facturas, delete_factura, ver_facturas


urlpatterns = [
    path('', facturas, name='facturas'),
    path('facturar/', create_factura, name='Create_factura'),
    path('ver_factura/', ver_facturas, name='Ver_facturas'),
    path('productos/', ver_facturas, name='Productos'),
    path('cleinte/', ver_facturas, name='Clientes'),
    path('proveedor/', ver_facturas, name='Provedores'),
    path('asistencia_contable/', ver_facturas, name='Asistencia_contable'),
    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]