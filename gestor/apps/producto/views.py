from datetime import date
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from gestor.apps.estado.models import estado as Estados
from gestor.apps.proveedor.models import (proveedor)
from gestor.apps.usuario.models import (Role, CustomUser)
from gestor.apps.inventario.models import (inventario, stock)
from .models import (producto, categoria, marca)
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


# ---------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Producto----------------------------------------------------------------------

@login_required
@vendedor_required
def menu_producto(request):
    marc = marca.objects.all()
    catg = categoria.objects.all()
    prov = proveedor.objects.all()
    user = request.user

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'create_product.html', {"marcas": marc, "categorias": catg,
                                                   "proveedores": prov, "user_role": user_role,
                                                   'user': user})


@login_required
@vendedor_required
def create_product(request):
    fecha_hoy = date.today()
    marcas = marca.objects.all()
    catgedorias = categoria.objects.all()
    proveedores = proveedor.objects.all()
    estados = Estados.objects.all()

    existe = producto.objects.filter(
        cod_producto=request.POST['cod_producto']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, 
                                                       "categorias": catgedorias, "proveedores": proveedores, "estados": estados})

    else:
        cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
        prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
        marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
        est = get_object_or_404(Estados, pk=1)

        produc = producto(cod_producto=request.POST['cod_producto'], precio_costo=request.POST['precio_compra'], precio_venta=request.POST['precio_venta'],
                          cod_categoria=cat, cod_proveedor=prov, cod_marca=marc, estado=est, descripcion=request.POST['desc_producto'])
        produc.save()

        product = get_object_or_404(
            producto, cod_producto=request.POST['cod_producto'])

        inv = inventario(fecha=fecha_hoy, cod_producto=product, descripcion='Primera carga de stock',
                         tipo_movimiento=True, cantidad=request.POST['cantidad_producto'])
        inv.save()

        mensaje_error = "Producto guardado!!"
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, 
                                                       "categorias": catgedorias, "proveedores": proveedores, "estados": estados})

