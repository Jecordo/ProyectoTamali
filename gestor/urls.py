from django.urls import path
from .views import (
    create_factura, facturar, delete_factura, ver_facturas, menu_principal, 
    create_product, create_proveedor, create_client, asistencia_contable, 
    menu_producto, buscar_producto, menu_libro_diario, cargar_libro_diario,
    modificar_libro_diario, descargar_libro
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
    path('busc_produc/', buscar_producto, name='buscar_producto'),

    path('asistencia_contable/', menu_libro_diario, name='Asistencia_contable'),
    path('cargar_libro_diario/', cargar_libro_diario, name='cargar_libro_diario'),
    path('modif_libro_diario/', modificar_libro_diario, name='modificar_libro_diario'),
    path('descagar_libro/', descargar_libro, name='descargar_libro'),

    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]