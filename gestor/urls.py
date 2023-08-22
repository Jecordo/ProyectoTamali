from django.urls import path
from .views import create_factura, facturas, delete_factura, ver_facturas


urlpatterns = [
    path('', facturas),
    path('facturar/', create_factura, name='Create_factura'),
    path('ver_factura/', ver_facturas, name='Ver_facturas'),
    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]