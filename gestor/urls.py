from django.urls import path
from .views import create_factura, facturas


urlpatterns = [
    path('', facturas),
    path('facturar/', create_factura, name='Create_factura'),
]