from datetime import date
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from gestor.apps.estado.models import estado as Estados
from gestor.apps.proveedor.models import (proveedor)
from gestor.apps.usuario.models import (Role, CustomUser)
from gestor.apps.inventario.models import (inventario, stock)
from .models import producto, categoria, marca
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required
from django.core.paginator import Paginator


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

    return render(request, 'Producto/create_product.html', {"marcas": marc, "categorias": catg,
                                                   "proveedores": prov, "user_role": user_role,
                                                   'user': user})


# ----------------------------------------- Nuevo producto ---------------------------------------------------------


@login_required
@vendedor_required
def create_product(request):
    fecha_hoy = date.today()

    existe = producto.objects.filter(
        cod_producto=request.POST['cod_producto']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return redirect(listar_productos)

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

        mensaje_error = "Producto guardado!!"
        return redirect(listar_productos)


# ----------------------------------------- Modificar producto ---------------------------------------------------------
    

@login_required
@vendedor_required
def modificar_producto(request):
    fecha_hoy = date.today()

    produc = get_object_or_404(producto, pk=request.POST['cod_producto'])

    if produc:    
        cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
        prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
        marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
        est = get_object_or_404(Estados, pk=1)

        produc.cod_producto = request.POST['cod_producto']
        produc.precio_costo=request.POST['precio_compra']
        produc.precio_venta=request.POST['precio_venta']
        produc.cod_categoria=cat
        produc.cod_proveedor=prov
        produc.cod_marca=marc
        produc.estado=est
        produc.descripcion=request.POST['desc_producto']

        produc.save()

        product = get_object_or_404(
            producto, cod_producto=request.POST['cod_producto'])

        inv = inventario(fecha=fecha_hoy, cod_producto=product, descripcion='Primera carga de stock',
                         tipo_movimiento=True, cantidad=request.POST['cantidad_producto'])
        inv.save()

        mensaje_error = "Producto guardado!!"
        return redirect(listar_productos)

    else:
        mensaje_error = "Producto no existe!!"
        return redirect(listar_productos)


# ----------------------------------------- Listar producto ---------------------------------------------------------


@login_required
@vendedor_required
def listar_productos(request):
    produc = producto.objects.all().order_by('cod_producto')
    user = request.user

    marc = marca.objects.all()
    catg = categoria.objects.all()
    prov = proveedor.objects.all()

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
            print(user_role)
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
            print(user_role)
    else:
        user_role = "Usuario no autenticado"

    tipo = categoria.objects.all()

    # Filtrar los productos

    if 'categoria_filter' in request.POST and request.POST['categoria_filter'] != '':
        produc = produc.filter(
            categoria=request.POST['categoria_filter'])

    if 'nombre_filter' in request.POST and request.POST['nombre_filter'] != '':
        produc = produc.filter(
            descripcion__icontains=request.POST['nombre_filter'])

    paginator = Paginator(produc, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Producto/create_product.html', {"productos": page_obj, "user_role": user_role, 'user': user,
                                                            "marcas": marc, "categorias": catg, "proveedores": prov})


# ------------------------------------ Anular producto ---------------------------------------

@login_required
@vendedor_required
def anular_producto(request, producto_id):
    factura_obj = get_object_or_404(producto, id=producto_id)
    est = get_object_or_404(Estados, id=2)
    
    if factura_obj.estado == est:
        estado_activo = get_object_or_404(Estados, id=1)
        factura_obj.estado = estado_activo
        factura_obj.save()
    
    else:
        estado_inactivo = get_object_or_404(Estados, id=2)
        factura_obj.estado = estado_inactivo
        factura_obj.save()
    
    return redirect(listar_productos)