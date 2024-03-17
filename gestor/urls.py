from django.urls import path
from gestor.apps.cliente import views as cliente
from gestor.apps.proveedor import views as proveedor
from gestor.apps.contable.cuenta import views as cuenta
from gestor.apps.contable.libro_diario import views as libro_diario
from gestor.apps.contable.libro_mayor import views as libro_mayor
from gestor.apps.estadistica import views as estadistica
from gestor.apps.inventario import views as inventario
from gestor.apps.producto import views as producto
from gestor.apps.usuario import views as usuario
from gestor.apps.factura import views as factura
from gestor import views

urlpatterns = [
    path('', views.menu_principal, name='Menu_principal'),
    path('get_chart/', estadistica.get_chart, name='get_chart'),
    path('get_chart2/', estadistica.get_chart2, name='get_chart2'),

    path('cerrar_secion/', views.cerrar_secion, name='cerrar_secion'),
    path('crear_user/', usuario.crear_user, name='crear_user'),
    path('listar_user/', usuario.listar_user, name='listar_user'),
    path('modificar_user/', usuario.modificar_user, name='modificar_user'),
    path('modificar_user_final/', usuario.modificar_user_final,
         name='modificar_user_final'),
    path('eliminar_user/', usuario.eliminar_user, name='eliminar_user'),

    path('facturar/', factura.facturar, name='facturas'),
    path('generar_factura/', factura.create_factura, name='Create_factura'),
    path('delete_factura/', factura.delete_factura, name='delete_factura'),

    path('carga_factura_detalle/', factura.cargar_factura_detalle, name='factura_detalle'),
    path('menu_factura_detalle/', factura.menu_factura_detalle,
         name='menu_factura_detalle'),

    path('finalizar_factura/', factura.finalizar_factura, name='finalizar_factura'),
    path('listar_factura/', factura.listar_factura, name='listar_factura'),
    path('imprimir_factura/', factura.imprimir_factura, name='imprimir_factura'),

    path('cancelar_factura/<int:factura_cabecera_id>/',
         factura.cancelar_factura, name='cancelar_factura'),
    #path('factura_libro/<int:factura_cabecera_id>/', factura.factura_libro, name='factura_libro'),

    path('menu_proveedor/', proveedor.menu_proveedor, name='menu_proveedor'),
    path('carga_proveedor/', proveedor.carga_proveedor, name='carga_proveedor'),
    path('modificar_proveedor/', proveedor.modificar_proveedor, name='modificar_proveedor'),

    path('menu_cliente/', cliente.menu_cliente, name='menu_cliente'),
    path('carga_cliente/', cliente.carga_cliente, name='carga_cliente'),
    path('modificar_cliente/', cliente.modificar_cliente, name='modificar_cliente'),

    path('menproduc/', producto.menu_producto, name='menu_producto'),
    path('producto/', producto.create_product, name='cargar_roducto'),
    #path('busc_produc/', producto.buscar_producto, name='buscar_producto'),

    path('stock/', inventario.StockListView, name='stock_list'),
    path('menu_iventario/', inventario.menu_iventario, name='menu_iventario'),
    path('cargar_inventario/', inventario.cargar_inventario, name='cargar_inventario'),

    path('menu_libro_diario/', libro_diario.menu_libro_diario, name='Asistencia_contable'),
    path('cargar_libro_diario/', libro_diario.cargar_libro_diario, name='cargar_libro_diario'),
    path('modif_libro_diario/', libro_diario.modificar_libro_diario,
         name='modificar_libro_diario'),

    path('menu_libro_mayor/', libro_mayor.menu_libro_mayor, name='menu_libro_mayor'),
    path('cargar_libro_mayor/', libro_mayor.cargar_libro_mayor, name='cargar_libro_mayor'),
    path('modif_libro_mayor/', libro_mayor.modificar_libro_mayor,
         name='modificar_libro_mayor'),

    path('menu_cuenta/', cuenta.menu_cuenta, name='menu_cuenta'),
    path('registrar_cuenta/', cuenta.registrar_cuenta, name='registrar_cuenta'),
    path('modificar_cuenta/', cuenta.modificar_cuenta, name='modificar_cuenta'),

    path('descargar_libro_mayor/', libro_mayor.descargar_libro_mayor,
         name='descargar_libro_mayor'),
    path('descagar_libro/', libro_diario.descargar_libro, name='descargar_libro'),
    #path('migrar_asientos/', libro_diario.migrar_asientos, name='migrar_asientos'),

    path('mod_libro_diario/', libro_diario.mod_libro_diario, name='mod_libro_diario'),

]
