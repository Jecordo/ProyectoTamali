from pyexpat.errors import messages
from django.shortcuts import render,  redirect
from gestor.apps.producto.models import producto, categoria, marca
from gestor.apps.usuario.models import Role, CustomUser
from .models import inventario, stock
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


@login_required
@vendedor_required
def menu_iventario(request):
    produc = producto.objects.all()
    Invent = inventario.objects.all()
    user = request.user

    paginator = Paginator(Invent, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'inventario.html', {"inventario": page_obj, "user_role": user_role,
                                               'user': user, 'productos': produc})


@login_required
@vendedor_required
def cargar_inventario(request):
    fecha_hoy = request.POST['fecha_emision']
    cantidad = request.POST['cantidad_producto']
    desc = request.POST['descripcion']
    refe = request.POST['cod_referecnia']
    mov = request.POST['tip_mov']

    if mov == "True":
        mov = True
    else:
        mov = False

    produc = get_object_or_404(producto, id=request.POST['cod_producto_id'])

    print(fecha_hoy)

    inv = inventario(fecha=fecha_hoy, cod_producto=produc, descripcion=desc, referencia=refe,
                     tipo_movimiento=mov, cantidad=cantidad)
    inv.save()

    messages.success(request, 'Se agrego '+produc.descripcion)

    return redirect(menu_iventario)


# ------------------------------------------------Stock...................................................................


@login_required
@vendedor_required
def StockListView(request):
    stocks = stock.objects.all().order_by('id')
    user = request.user

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    categorias = categoria.objects.all()
    marcas = marca.objects.all()

    # Filtrar los productos

    if 'categoria_filter' in request.POST and request.POST['categoria_filter'] != '':
        stocks = stocks.filter(
            producto__cod_categoria__id=request.POST['categoria_filter'])

    if 'marca_filter' in request.POST and request.POST['marca_filter'] != '':
        stocks = stocks.filter(
            producto__cod_marca__id=request.POST['marca_filter'])

    if 'nombre_filter' in request.POST and request.POST['nombre_filter'] != '':
        stocks = stocks.filter(
            producto__descripcion__icontains=request.POST['nombre_filter'])

    paginator = Paginator(stocks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'stock_list.html', {"stock": page_obj, "user_role": user_role, 'user': user,
                                               "categorias": categorias, "marcas": marcas})
