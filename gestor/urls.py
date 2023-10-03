from django.urls import path
from .views import (
    create_factura, facturar, delete_factura, ver_facturas, menu_principal, 
    create_product, create_proveedor, create_client, asistencia_contable, 
    menu_producto, buscar_producto, menu_libro_diario, cargar_libro_diario,
    modificar_libro_diario, descargar_libro, menu_libro_mayor, cargar_libro_mayor,
    modificar_libro_mayor, migrar_asientos, menu_cuenta, registrar_cuenta, modificar_cuenta
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

    path('menu_libro_diario/', menu_libro_diario, name='Asistencia_contable'),
    path('cargar_libro_diario/', cargar_libro_diario, name='cargar_libro_diario'),
    path('modif_libro_diario/', modificar_libro_diario, name='modificar_libro_diario'),

    path('menu_libro_mayor/', menu_libro_mayor, name='menu_libro_mayor'),
    path('cargar_libro_mayor/', cargar_libro_mayor, name='cargar_libro_mayor'),
    path('modif_libro_mayor/', modificar_libro_mayor, name='modificar_libro_mayor'),

    path('menu_cuenta/', menu_cuenta, name='menu_cuenta'),
    path('registrar_cuenta/', registrar_cuenta, name='registrar_cuenta'),
    path('modificar_cuenta/', modificar_cuenta, name='modificar_cuenta'),

    path('descagar_libro/', descargar_libro, name='descargar_libro'),
    path('migrar_asientos/', migrar_asientos, name='migrar_asientos'),    

    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]