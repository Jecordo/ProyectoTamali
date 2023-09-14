from django.urls import path
from .views import (
    create_factura, facturar, delete_factura, ver_facturas, menu_principal, 
    create_product, create_proveedor, create_client, asistencia_contable, 
    menu_producto, busca_producto
)

urlpatterns = [
    path('', menu_principal, name='Menu_principal'),
    path('facturar/', facturar, name='facturas'),
    path('generar_factura/', create_factura, name='Create_factura'),
    path('ver_factura/', ver_facturas, name='Ver_facturas'),
    path('client/', create_client, name='Clientes'),
    path('proveedor/', create_proveedor, name='Provedores'),

    path('menproduc/', menu_producto, name='menu_producto'),
    path('producto/', create_product, name='cargar_roducto'),
    path('busc_produc/<str:cod_producto>/', busca_producto, name='buscar_producto'),

    path('asistencia_contable/', asistencia_contable, name='Asistencia_contable'),
    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]