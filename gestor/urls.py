from django.urls import path
from .views import create_factura, facturas, delete_factura


urlpatterns = [
    path('', facturas),
    path('facturar/', create_factura, name='Create_factura'),
    path('delete_factura/<int:factu_id>/', delete_factura, name='Delete_factura'),
]