from django.urls import path
from .views import (
    create_factura, facturar, delete_factura, menu_principal,
    create_product, menu_cliente, menu_proveedor, carga_proveedor, modificar_proveedor,
    menu_producto, buscar_producto, menu_libro_diario, cargar_libro_diario,
    modificar_libro_diario, descargar_libro, menu_libro_mayor, cargar_libro_mayor,
    modificar_libro_mayor, migrar_asientos, menu_cuenta, registrar_cuenta, modificar_cuenta,
    cargar_factura_detalle, delete_factura, menu_factura_detalle, cancelar_factura,
    modificar_cliente, carga_cliente, descargar_libro_mayor, factura_libro,
    mod_libro_diario
)
from . import views

urlpatterns = [
    path('', menu_principal, name='Menu_principal'),
    path('get_chart/', views.get_chart, name='get_chart'),
    path('get_chart2/', views.get_chart2, name='get_chart2'),

    path('cerrar_secion/', views.cerrar_secion, name='cerrar_secion'),
    path('crear_user/', views.crear_user, name='crear_user'),
    path('listar_user/', views.listar_user, name='listar_user'),
    path('modificar_user/', views.modificar_user, name='modificar_user'),
    path('modificar_user_final/', views.modificar_user_final,
         name='modificar_user_final'),
    path('eliminar_user/', views.eliminar_user, name='eliminar_user'),

    path('facturar/', facturar, name='facturas'),
    path('generar_factura/', create_factura, name='Create_factura'),
    path('delete_factura/', delete_factura, name='delete_factura'),
    path('carga_factura_detalle/', cargar_factura_detalle, name='factura_detalle'),
    path('menu_factura_detalle/', menu_factura_detalle,
         name='menu_factura_detalle'),
    path('finalizar_factura/', views.finalizar_factura, name='finalizar_factura'),

    path('cancelar_factura/<int:factura_cabecera_id>/',
         cancelar_factura, name='cancelar_factura'),
    path('factura_libro/<int:factura_cabecera_id>/',
         factura_libro, name='factura_libro'),

    path('menu_proveedor/', menu_proveedor, name='menu_proveedor'),
    path('carga_proveedor/', carga_proveedor, name='carga_proveedor'),
    path('modificar_proveedor/', modificar_proveedor, name='modificar_proveedor'),

    path('menu_cliente/', menu_cliente, name='menu_cliente'),
    path('carga_cliente/', carga_cliente, name='carga_cliente'),
    path('modificar_cliente/', modificar_cliente, name='modificar_cliente'),

    path('menproduc/', menu_producto, name='menu_producto'),
    path('producto/', create_product, name='cargar_roducto'),
    path('busc_produc/', buscar_producto, name='buscar_producto'),

    path('stock/', views.StockListView, name='stock_list'),
    path('menu_iventario/', views.menu_iventario, name='menu_iventario'),
    path('cargar_inventario/', views.cargar_inventario, name='cargar_inventario'),

    path('menu_libro_diario/', menu_libro_diario, name='Asistencia_contable'),
    path('cargar_libro_diario/', cargar_libro_diario, name='cargar_libro_diario'),
    path('modif_libro_diario/', modificar_libro_diario,
         name='modificar_libro_diario'),

    path('menu_libro_mayor/', menu_libro_mayor, name='menu_libro_mayor'),
    path('cargar_libro_mayor/', cargar_libro_mayor, name='cargar_libro_mayor'),
    path('modif_libro_mayor/', modificar_libro_mayor,
         name='modificar_libro_mayor'),

    path('menu_cuenta/', menu_cuenta, name='menu_cuenta'),
    path('registrar_cuenta/', registrar_cuenta, name='registrar_cuenta'),
    path('modificar_cuenta/', modificar_cuenta, name='modificar_cuenta'),

    path('descargar_libro_mayor/', descargar_libro_mayor,
         name='descargar_libro_mayor'),
    path('descagar_libro/', descargar_libro, name='descargar_libro'),
    path('migrar_asientos/', migrar_asientos, name='migrar_asientos'),

    path('mod_libro_diario/', mod_libro_diario, name='mod_libro_diario'),

]
