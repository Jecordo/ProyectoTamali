from audioop import reverse
from datetime import date
import json
from pyexpat.errors import messages
import re
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render,  redirect
from .models import (
    Role, CustomUser, factura, factura_detalle, cliente, producto,
    categoria, marca, Estados, proveedor, tipo_factura,
    metodo_pago, marca, cuenta, libro_diario, detalle_libro_diario,
    libro_mayor)
from django.shortcuts import get_object_or_404
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Cast
from django.db.models import CharField
from django.db.models import Q
from django.core.paginator import Paginator, Page
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .decorators import admin_required, vendedor_required, contador_required
from urllib.parse import quote, unquote


@login_required
def cerrar_secion(request):
    logout(request)
    return redirect(menu_principal)


@login_required
def menu_principal(request):
    user = request.user

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'dashboard.html', {'user_role': user_role, 'user': user})


@login_required
@admin_required
def crear_user(request):
    user = request.user

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    if request.method == 'GET':
        return render(request, 'crear_user.html', {'user_role': user_role, 'user': user})

    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nombre = request.POST['nombre', '']
        apellido = request.POST['apellido', '']
        email = request.POST['email', '']

        if password1 == password2:
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El usuario ya existe.')
            else:
                # Usuario no existe, proceder con la creación
                user = User.objects.create_user(
                    username=username, password=password1)
                # Asigna el rol adecuado
                role = Role.objects.get(name=request.POST['rols'])
                custom_user = CustomUser.objects.create(user=user, role=role, nombre=nombre,
                                                        apellido=apellido, email=email)
                custom_user.save()
                messages.success(request, 'Usuario Guardado.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

        return redirect(crear_user)


@login_required
@admin_required
def listar_user(request):
    usuarios = CustomUser.objects.all()
    user = request.user

    paginator = Paginator(usuarios, 10)

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

    return render(request, 'listar_usuarios.html', {'user_role': user_role, 'user': user, 'usuarios': page_obj})


@login_required
@admin_required
def assign_role_to_user(request, user_id, role_name):
    user = User.objects.get(id=user_id)
    role, created = Role.objects.get_or_create(name=role_name)
    user.role = role
    user.save()

# -----------------------------------Factura----------------------------------------------
# ----------------------------------------------------------------------------------------


@login_required
@vendedor_required
def facturar(request):
    user = request.user
    client = cliente.objects.all()
    metodo = metodo_pago.objects.all()
    tipo = tipo_factura.objects.all()
    factu_prduc = []

    ultimoa_factura = factura.objects.all().exists()

    if ultimoa_factura:
        ultimoa_factura = factura.objects.order_by('-num_factura').first()
        num_factura = int(ultimoa_factura.num_factura) + 1
        num_factura = f"{num_factura:07d}"
    else:
        num_factura = 1
        num_factura = f"{num_factura:07d}"

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'create_factura.html', {"clientes": client, "ultima_factura": num_factura,
                                                   "factu_prduc": factu_prduc, "metodos_pagos": metodo,
                                                   'tipos_facturas': tipo, 'user_role': user_role})


@login_required
@vendedor_required
def factura_libro(request, factura_cabecera_id):
    fecha_hoy = date.today()

    factura_cabecera = get_object_or_404(factura, pk=factura_cabecera_id)
    factu_detalle = factura_detalle.objects.filter(
        num_factura=factura_cabecera.id).order_by('id')

    for detalle in factu_detalle:

        if libro_diario.objects.all().exists():
            asiento = libro_diario.objects.order_by('-num_asiento').first()
            asiento = asiento.num_asiento
        else:
            asiento = 0

        concep_1 = 'Ventas del '+str(fecha_hoy) + \
            ', '+detalle.cod_producto.descripcion
        cta_1 = cuenta.objects.filter(descripcion='Venta').first()
        concep_2 = 'IVA credito fiscal 10%'
        cta_2 = cuenta.objects.filter(
            descripcion='IVA credito fiscal 10%').first()
        concep_3 = 'Por la venta de producto '+detalle.cod_producto.cod_producto
        cta_3 = cuenta.objects.filter(descripcion='Mercaderia').first()

        iva = int(detalle.total_precio)-int(detalle.impuesto)

        libro = libro_diario(fecha=fecha_hoy, num_asiento=asiento+1, concepto=concep_1,
                             num_cuenta=cta_1, debe=iva, haber=0)
        libro.save()

        libro = libro_diario(fecha=fecha_hoy, num_asiento=asiento+1, concepto=concep_2,
                             num_cuenta=cta_2, debe=detalle.impuesto, haber=0)
        libro.save()

        libro = libro_diario(fecha=fecha_hoy, num_asiento=asiento+1, concepto=concep_3,
                             num_cuenta=cta_3, debe=0, haber=detalle.total_precio)
        libro.save()

    return redirect(menu_libro_diario)


@login_required
@vendedor_required
def create_factura(request):
    prod = producto.objects.all()
    existe = factura.objects.filter(
        num_factura=request.POST['num_factura']).exists()

    if existe:
        messages.error(request, 'Numero de factura ya registrado')
        return redirect(facturar)
    else:
        existe = cliente.objects.filter(
            RUC=request.POST['ruc_cliente']).exists()

        if existe:
            aux_cliente = get_object_or_404(
                cliente, RUC=request.POST['ruc_cliente'])

            aux_cliente.razon_social = request.POST['razon_social']
            aux_cliente.direccion = request.POST['direccion_cliente']
            aux_cliente.correo = request.POST['correo_cliente']
            aux_cliente.num_telefono = request.POST['num_telefono']

            aux_cliente.save()

            messages.success(request, 'Cabecera generada')
        else:
            est = get_object_or_404(Estados, pk=1)

            aux_cliente = cliente(RUC=request.POST['ruc_cliente'], razon_social=request.POST['razon_social'], direccion=request.POST['direccion_cliente'],
                                  correo=request.POST['correo_cliente'], num_telefono=request.POST['num_telefono'], estado=est)

            aux_cliente.save()
            messages.success(request, 'Cabecera generada - Cliente creado')

    est = get_object_or_404(Estados, pk=1)
    ment_pag = get_object_or_404(metodo_pago, pk=request.POST['metodo_pago'])
    client = get_object_or_404(cliente, RUC=request.POST['ruc_cliente'])
    factura_tipo = get_object_or_404(
        tipo_factura, pk=request.POST['tipo_factura'])

    factura_cabecera = factura(num_factura=request.POST['num_factura'], cliente=client, tipo_factura=factura_tipo,
                               metodo_de_pago=ment_pag, estado=est, timbrado=request.POST['timbrado_factura'])
    factura_cabecera.save()

    factura_cabecera_id_encoded = quote(str(factura_cabecera.id))

    return redirect(menu_factura_detalle, factura_cabecera_id=factura_cabecera_id_encoded)

# -----------------------------------Detalle de la factura----------------------------------------------


@login_required
@vendedor_required
def menu_factura_detalle(request, factura_cabecera_id):
    factura_cabecera_id = unquote(factura_cabecera_id)
    user = request.user

    productos = producto.objects.all()
    factura_cabecera = get_object_or_404(factura, pk=factura_cabecera_id)

    factu_detalle = factura_detalle.objects.filter(
        num_factura=factura_cabecera.id).order_by('id')

    suma = 0
    suma_iva = 0
    for precio in factu_detalle:
        suma = suma + precio.total_precio
        suma_iva = suma_iva + precio.cod_producto.iva_producto

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'create_factura_detalle.html', {"factura_cabecera": factura_cabecera, "productos": productos,
                                                           "facturas_detalles": factu_detalle, "total_compra": suma, "total_iva": suma_iva,
                                                           'user_role': user_role, 'user': user})


@login_required
@vendedor_required
def cargar_factura_detalle(request):
    factu = get_object_or_404(factura, num_factura=request.POST['num_factura'])
    produc = get_object_or_404(
        producto, pk=int(request.POST['cod_producto_id']))

    existe = factura_detalle.objects.filter(
        cod_producto=produc.id, num_factura=factu.id).exists()

    if existe:
        factu_detalle = get_object_or_404(factura_detalle, Q(
            cod_producto=produc.id) & Q(num_factura=factu.id))
        factu_detalle.cantidad = factu_detalle.cantidad + 1
        factu_detalle.total_precio = factu_detalle.cantidad * \
            factu_detalle.cod_producto.precio_venta
        factu_detalle.impuesto = factu_detalle.cantidad * \
            factu_detalle.cod_producto.iva_producto
        factu_detalle.save()

        messages.success(request, 'Se agrego un/a ' +
                         produc.descripcion + ' a la cantidad')
    else:
        factu_detalle = factura_detalle(cod_producto=produc, num_factura=factu, total_precio=produc.precio_venta,
                                        cantidad=1, impuesto=produc.iva_producto)

        factu_detalle.save()

        messages.success(request, 'Se agrego '+produc.descripcion)

    return redirect(menu_factura_detalle, factura_cabecera_id=factu.id)


@login_required
@vendedor_required
def delete_factura(request):
    prod = producto.objects.all()
    factu_detalle = get_object_or_404(
        factura_detalle, pk=int(request.POST['id_detalle']))
    num_factura = factu_detalle.num_factura
    factu_detalle.delete()

    factu_detalles = factura_detalle.objects.filter(
        num_factura=num_factura).order_by('id')

    suma = 0
    for precio in factu_detalles:
        suma = suma + precio.total_precio

    factu_cabecera = get_object_or_404(factura, num_factura=num_factura)

    return render(request, 'create_factura_detalle.html', {"factura_cabecera": factu_cabecera, "productos": prod,
                                                           "facturas_detalles": factu_detalles, "total_compra": suma})


@login_required
@vendedor_required
def cancelar_factura(request, factura_cabecera_id):

    factura_cabecera = get_object_or_404(factura, pk=factura_cabecera_id)
    factu_detalle = factura_detalle.objects.filter(
        num_factura=factura_cabecera.id).order_by('id')
    factu_detalle.delete()
    factura_cabecera.delete()

    return redirect(facturar)


@login_required
@vendedor_required
def ver_facturas(request):
    factu = persona.objects.all()
    return render(request, 'listar_facturas.html', {"personas": factu})


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
    marcas = marca.objects.all()
    catgedorias = categoria.objects.all()
    proveedores = proveedor.objects.all()
    estados = Estados.objects.all()

    existe = producto.objects.filter(
        cod_producto=request.POST['cod_producto']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})

    else:
        cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
        prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
        marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
        est = get_object_or_404(Estados, pk=1)

        produc = producto(cod_producto=request.POST['cod_producto'], precio_costo=request.POST['precio_compra'], precio_venta=request.POST['precio_venta'],
                          cod_categoria=cat, cod_proveedor=prov, cod_marca=marc, estado=est, descripcion=request.POST['desc_producto'])
        produc.save()

        mensaje_error = "Producto guardado!!"
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})


@login_required
@vendedor_required
def buscar_producto(request):
    objetos = producto.objects.all().values_list('cod_producto', flat=True)
    return JsonResponse(list(objetos), safe=False)

# -------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Libro diario----------------------------------------------------------------------


@login_required
@contador_required
def menu_libro_diario(request):
    fecha_hoy = date.today()
    user = request.user

    libros_diarios = libro_diario.objects.filter(
        fecha__year=fecha_hoy.year).order_by('num_asiento')
    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_diarios, 10)

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

    return render(request, 'cargar_asiento_diario.html', {"libros_diarios": page_obj, "cuentas": cuentas,
                                                          "user_role": user_role, 'user': user})


@csrf_exempt
@login_required
@contador_required
def cargar_libro_diario(request):
    conceptos_str = request.POST.get('concepto', '')
    cuentas_str = request.POST.get('cuenta', '')
    debes_str = request.POST.get('debe', '')
    haberes_str = request.POST.get('haber', '')

    fecha = request.POST['fecha_emision_hidden']

    # Divide las cadenas en listas
    conceptos = conceptos_str.split(",")
    cuentas = cuentas_str.split(",")
    debes = debes_str.split(",")
    haberes = haberes_str.split(",")

    if libro_diario.objects.all().exists():
        asiento = libro_diario.objects.order_by('-num_asiento').first()
        asiento = asiento.num_asiento + 1
    else:
        asiento = 1

    cab_lib = libro_diario(concepto=conceptos[1], num_asiento=asiento)
    cab_lib.save()

    cab_lib = get_object_or_404(libro_diario, num_asiento=asiento)

    for i in range(1, len(conceptos)):
        concepto = conceptos[i]
        num_cuenta = cuentas[i]
        cta = get_object_or_404(cuenta, num_cuenta=num_cuenta)

        if debes[i]:
            debe = int(debes[i])
        else:
            debe = 0
        if haberes[i]:
            haber = int(haberes[i])
        else:
            haber = 0

        deta_lib = detalle_libro_diario(
            num_asiento=cab_lib, concepto=concepto, num_cuenta=cta, debe=debe, haber=haber)
        deta_lib.save()

    cab_lib.fecha = fecha
    cab_lib.save()

    messages.success(request, 'Asiento guardado!!')
    return redirect(menu_libro_diario)


@login_required
@contador_required
def equilibrio():
    if libro_diario.objects.all().exists():
        aux_lib = libro_diario.objects.order_by('-id').first()

        corroboration = libro_diario.objects.filter(
            num_asiento=aux_lib.num_asiento)
        suma = 0

        for lib in corroboration:
            suma = suma + lib.debe
            suma = suma - lib.haber
    else:
        suma = 0

    return int(suma)


@login_required
@contador_required
def mod_libro_diario(request):
    cabecera_libro = get_object_or_404(
        libro_diario, pk=request.POST['id_libro'])
    detalle_libro = detalle_libro_diario.objects.filter(
        num_asiento=cabecera_libro.num_asiento)
    cuentas = cuenta.objects.all()

    detalle_libro_list = [detalle.to_dict() for detalle in detalle_libro]
    detalle_libro_json = json.dumps(detalle_libro_list)

    return render(request, 'modificar_asiento_diario.html', {"cuentas": cuentas, "cabe_lib": cabecera_libro, "deta_lib": detalle_libro_json})


@never_cache
@login_required
@contador_required
def modificar_libro_diario(request):
    asiento_cab = request.POST['asiento']
    fecha = request.POST['fecha_emision_hidden']

    existe = libro_diario.objects.filter(num_asiento=asiento_cab).exists()

    if existe:
        aux_libro = get_object_or_404(libro_diario, num_asiento=asiento_cab)

        aux_detalle = detalle_libro_diario.objects.filter(
            num_asiento=asiento_cab)

        aux_detalle.delete()

        conceptos_str = request.POST.get('concepto', '')
        cuentas_str = request.POST.get('cuenta', '')
        debes_str = request.POST.get('debe', '')
        haberes_str = request.POST.get('haber', '')

        conceptos = conceptos_str.split(",")
        cuentas = cuentas_str.split(",")
        debes = debes_str.split(",")
        haberes = haberes_str.split(",")

        aux_libro.concepto = conceptos[1]
        aux_libro.fecha = fecha

        aux_libro.save()

        cab_lib = get_object_or_404(libro_diario, num_asiento=asiento_cab)

        for i in range(1, len(conceptos)):
            concepto = conceptos[i]
            num_cuenta = cuentas[i]
            cta = get_object_or_404(cuenta, num_cuenta=num_cuenta)

            if debes[i]:
                debe = int(debes[i])
            else:
                debe = 0
            if haberes[i]:
                haber = int(haberes[i])
            else:
                haber = 0

            deta_lib = detalle_libro_diario(
                num_asiento=cab_lib, concepto=concepto, num_cuenta=cta, debe=debe, haber=haber)
            deta_lib.save()

        messages.success(request, 'Asiento modificado!!')
        return redirect(menu_libro_diario)
    else:
        messages.error(request, 'Asiento no esta cargado.')

        return redirect(menu_libro_diario)


@never_cache
@login_required
@contador_required
def descargar_libro(request):
    fecha_libro = request.POST['fecha_deseada']

    if re.match(r'^\d{4}-(0[1-9]|1[0-2])$', fecha_libro):
        year, month = map(int, fecha_libro.split('-'))

        datos = libro_diario.objects.filter(Q(fecha__year=year) & Q(
            fecha__month=month)).order_by('fecha', 'num_asiento')

    else:
        year = int(fecha_libro)
        print(year)

        datos = libro_diario.objects.filter(
            fecha__year=year).order_by('fecha', 'num_asiento')

    df = pd.DataFrame(list(datos.values('fecha', 'num_asiento',
                      'concepto', 'num_cuenta', 'debe', 'haber')))

    libro_excel = Workbook()

    hoja = libro_excel.active

    for fila in dataframe_to_rows(df, index=False, header=True):
        hoja.append(fila)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libro diario.xlsx'

    libro_excel.save(response)

    return response


@login_required
@contador_required
def migrar_asientos(request):
    asientos_migrar = detalle_libro_diario.objects.all().order_by('num_asiento')
    libros_mayores = libro_mayor.objects.all()

    libros_mayores.delete()

    for asiento in asientos_migrar:
        libro_mayor_mas_reciente = libro_mayor.objects.filter(
            num_cuenta=asiento.num_cuenta).order_by('-id').first()

        if libro_mayor_mas_reciente:
            saldo = libro_mayor_mas_reciente.saldo + asiento.debe
            saldo = saldo - asiento.haber
        else:
            saldo = asiento.debe
            saldo = saldo - asiento.haber

        libro = libro_mayor(fecha=asiento.num_asiento.fecha, num_asiento=asiento.num_asiento.num_asiento, concepto=asiento.concepto,
                            num_cuenta=asiento.num_cuenta, debe=asiento.debe, haber=asiento.haber, saldo=saldo)

        libro.save()

    messages.success(request, 'Asiento guardado!!')
    return redirect(menu_libro_mayor)


@login_required
@contador_required
def llamar_funcion_django(request):
    # Realiza cualquier lógica necesaria aquí

    # Genera un enlace a la página HTML que deseas abrir en una nueva pestaña
    enlace_html = '/carga_cuenta.html'  # Reemplaza con la ruta correcta

    # Devuelve una respuesta JSON con el enlace
    return JsonResponse({'enlace_html': enlace_html})

# -------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Libro mayor----------------------------------------------------------------------


@never_cache
@login_required
@contador_required
def menu_libro_mayor(request):
    fecha_hoy = date.today()
    user = request.user

    if 'num_cuenta' in request.POST:
        libros_mayores = libro_mayor.objects.filter(
            num_cuenta=request.POST['num_cuenta'], fecha__year=fecha_hoy.year).order_by('num_asiento', 'num_cuenta')
    else:
        if libro_mayor.objects.all().exists():
            lib = libro_mayor.objects.order_by('-fecha').first()
            libros_mayores = libro_mayor.objects.filter(
                num_cuenta=lib.num_cuenta).order_by('num_asiento', 'num_cuenta')
        else:
            libros_mayores = libro_mayor.objects.all()

    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_mayores, 10)
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

    return render(request, 'cargar_asiento_mayor.html', {"libros_mayores": page_obj, "cuentas": cuentas,
                                                         'user_role': user_role, 'user': user})


@never_cache
@login_required
@contador_required
def cargar_libro_mayor(request):
    fecha_hoy = date.today()

    libros_mayores = libro_mayor.objects.filter(
        fecha__year=fecha_hoy.year).order_by('fecha', 'num_asiento')
    cuentas = cuenta.objects.all()

    existe = libro_mayor.objects.filter(
        num_asiento=request.POST['num_asiento'], num_cuenta=request.POST['num_cuenta']).exists()

    if existe:
        return redirect(menu_libro_mayor)

    else:
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'])
        libro_mayor_mas_reciente = libro_mayor.objects.order_by(
            '-fecha').first()
        tipo_mov = request.POST['tipo_movimiento']

        if tipo_mov == "1":
            if libro_mayor_mas_reciente:
                saldo = libro_mayor_mas_reciente.saldo + \
                    int(request.POST['id_monto'])
            else:
                saldo = int(request.POST['id_monto'])

            libro = libro_mayor(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento'],
                                concepto=request.POST['id_concepto'], num_cuenta=cta, debe=request.POST['id_monto'], haber=0, saldo=saldo)

            libro.save()

        elif tipo_mov == "2":
            if libro_mayor_mas_reciente:
                saldo = libro_mayor_mas_reciente.saldo + \
                    int(request.POST['id_monto'])
            else:
                saldo = int(request.POST['id_monto'])

            libro = libro_mayor(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento'],
                                concepto=request.POST['id_concepto'], num_cuenta=cta, debe=0, haber=request.POST['id_monto'], saldo=saldo)

            libro.save()

        messages.success(request, 'Asiento guardado!!')
        return redirect(menu_libro_mayor)


@never_cache
@login_required
@contador_required
def modificar_libro_mayor(request):
    id_libro = request.POST['id_libro']
    cont = 0

    libros_mayores = libro_mayor.objects.filter(
        pk__gte=id_libro).order_by('num_asiento')

    existe = libro_mayor.objects.filter(id=id_libro).exists()

    if existe:
        aux_libro = get_object_or_404(libro_mayor, pk=id_libro)
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'+id_libro])

        if aux_libro.debe == int(request.POST['monto_debe'+id_libro]) and aux_libro.haber == int(request.POST['monto_haber'+id_libro]):

            aux_libro.fecha = request.POST['fecha_emision'+id_libro]
            aux_libro.num_asiento = request.POST['num_asiento'+id_libro]
            aux_libro.concepto = request.POST['id_concepto'+id_libro]
            aux_libro.num_cuenta = cta

            aux_libro.save()

        else:
            libro_mayor_mas_reciente = obtener_libro_mayor_anterior(id_libro)
            saldo_agregado = int(request.POST['monto_debe'+id_libro])
            saldo_agregado = saldo_agregado - \
                int(request.POST['monto_haber'+id_libro])

            if libro_mayor_mas_reciente:
                aux_libro.saldo = libro_mayor_mas_reciente.saldo + saldo_agregado
            else:
                aux_libro.saldo = saldo_agregado

            aux_libro.fecha = request.POST['fecha_emision'+id_libro]
            aux_libro.num_asiento = request.POST['num_asiento'+id_libro]
            aux_libro.concepto = request.POST['id_concepto'+id_libro]
            aux_libro.debe = request.POST['monto_debe'+id_libro]
            aux_libro.haber = request.POST['monto_haber'+id_libro]
            aux_libro.num_cuenta = cta

            aux_libro.save()

            for libro in libros_mayores[1:]:
                saldo_agregado = libro.debe
                saldo_agregado = saldo_agregado - libro.haber
                libro.saldo = libros_mayores[cont].saldo + saldo_agregado

                libro.save()
                cont += 1

        messages.success(request, 'Asiento actualizado!!')
        return redirect(menu_libro_mayor)
    else:
        messages.error(request, 'Asiento no esta cargado.')

        return redirect(menu_libro_mayor)


@login_required
@contador_required
def obtener_libro_mayor_anterior(id_libro):
    try:
        libro_mayor_anterior = libro_mayor.objects.filter(
            pk__lt=id_libro).latest('pk')
        return libro_mayor_anterior
    except libro_mayor.DoesNotExist:
        return None


@never_cache
@login_required
@contador_required
def descargar_libro_mayor(request):
    fecha_libro = request.POST['fecha_libro']

    if re.match(r'^\d{4}-(0[1-9]|1[0-2])$', fecha_libro):
        year, month = map(int, fecha_libro.split('-'))

        datos = libro_mayor.objects.filter(Q(fecha__year=year) & Q(
            fecha__month=month)).order_by('fecha', 'num_asiento')

    else:
        year = int(fecha_libro)
        month = 1

        datos = libro_mayor.objects.all().order_by('fecha', 'num_asiento')

    df = pd.DataFrame(list(datos.values('fecha', 'num_asiento',
                      'concepto', 'num_cuenta', 'debe', 'haber', 'saldo')))

    libro_excel = Workbook()

    hoja = libro_excel.active

    for fila in dataframe_to_rows(df, index=False, header=True):
        hoja.append(fila)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libro mayor.xlsx'

    libro_excel.save(response)

    return response


# ----------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Cuentas----------------------------------------------------------------------

@never_cache
@login_required
@contador_required
def menu_cuenta(request):
    user = request.user
    cuentas = cuenta.objects.all().order_by('id')

    paginator = Paginator(cuentas, 1)

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

    return render(request, 'carga_cuenta.html', {"cuentas": page_obj, 'user_role': user_role, 'user': user})


@never_cache
@login_required
@contador_required
def registrar_cuenta(request):
    fecha_hoy = date.today()

    existe = cuenta.objects.filter(
        num_cuenta=request.POST['num_cuenta']).exists()

    if equilibrio() == 0:
        if existe:
            messages.error(request, 'Cuenta ya existe!!')
            return redirect(menu_cuenta)

        else:
            cta = cuenta(num_cuenta=request.POST['num_cuenta'],
                         descripcion=request.POST['nom_cuenta'], saldo=request.POST['id_monto'])
            cta.save()

            if cuenta.objects.filter(num_cuenta='999999999').exists():
                aux = cuenta.objects.filter(
                    descripcion='Capital del titular').first()
                cta_salida = get_object_or_404(
                    cuenta, num_cuenta=aux.num_cuenta)
            else:
                cta_salida = cuenta(
                    num_cuenta='999999999', descripcion='Capital del titular', saldo=request.POST['id_monto'])
                cta_salida.save()

            concepto_entrada = "Creación de cuenta " + cta.descripcion
            concepto_salida = 'Aporte capital'

            if libro_diario.objects.all().exists():
                asiento = libro_diario.objects.order_by('-num_asiento').first()
                asiento = int(asiento.num_asiento)+1
            else:
                asiento = 1

            if int(cta.saldo) > 0:
                libro = libro_diario(fecha=fecha_hoy, num_asiento=asiento, concepto=concepto_salida,
                                     num_cuenta=cta_salida, debe=0, haber=int(cta.saldo))
                libro.save()

                libro = libro_diario(fecha=fecha_hoy, num_asiento=asiento,
                                     concepto=concepto_entrada, num_cuenta=cta, debe=cta.saldo, haber=0)
                libro.save()

            messages.success(request, 'Cuenta guardada!!')
            return redirect(menu_cuenta)
    else:
        messages.error(
            request, 'Cuenta no se pudo registrar por falta de equilibrio en el asiento de libro diario!!')

        return redirect(menu_cuenta)


@never_cache
@login_required
@contador_required
def modificar_cuenta(request):
    id_cuenta = request.POST['id_cuenta']

    existe = cuenta.objects.filter(id=request.POST['id_cuenta']).exists()

    if existe:
        aux_cuenta = get_object_or_404(cuenta, pk=request.POST['id_cuenta'])

        aux_cuenta.num_cuenta = request.POST['num_cuenta'+id_cuenta]
        aux_cuenta.descripcion = request.POST['nom_cuenta'+id_cuenta]
        aux_cuenta.saldo = request.POST['id_monto'+id_cuenta]

        aux_cuenta.save()

        messages.success(request, 'Cuenta actualizada!!')
        return redirect(menu_cuenta)
    else:
        messages.error(request, 'Cuenta no existe!!')

        return redirect(menu_cuenta)


# -------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Proveedor----------------------------------------------------------------------

@login_required
@vendedor_required
def menu_proveedor(request):
    user = request.user
    prov = proveedor.objects.all()

    paginator = Paginator(prov, 10)

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

    return render(request, 'carga_proveedor.html', {"proveedores": page_obj, 'user_role': user_role, 'user': user})


@login_required
@vendedor_required
def carga_proveedor(request):
    est = get_object_or_404(Estados, pk=1)

    existe = proveedor.objects.filter(
        RUC=request.POST['ruc_proveedor']).exists()

    if existe:
        messages.error(request, 'El proveedor ya esta cargado.')
        return redirect(menu_proveedor)

    else:
        prov = proveedor(RUC=request.POST['ruc_proveedor'], nombre=request.POST['nombre_proveedor'], razon_social=request.POST['razon_social'],
                         direccion=request.POST['direccion_proveedor'], correo=request.POST['correo_proveedor'], estado=est, num_telefono=request.POST['num_telefono'],)
        prov.save()

        messages.success(request, 'Proveedor cargado!!')
        return redirect(menu_proveedor)


@login_required
@vendedor_required
def modificar_proveedor(request):
    id_proveedor = request.POST['id_proveedor']

    existe = proveedor.objects.filter(id=request.POST['id_proveedor']).exists()

    if existe:
        est = Estados.objects.filter(
            id=request.POST['estado_proveedor'+id_proveedor]).exists()

        aux_proveedor = get_object_or_404(
            proveedor, pk=request.POST['id_proveedor'])

        aux_proveedor.RUC = request.POST['ruc_proveedor'+id_proveedor]
        aux_proveedor.nombre = request.POST['nombre_proveedor'+id_proveedor]
        aux_proveedor.razon_social = request.POST['razon_social'+id_proveedor]
        aux_proveedor.direccion = request.POST['direccion_proveedor'+id_proveedor]
        aux_proveedor.correo = request.POST['correo_proveedor'+id_proveedor]
        aux_proveedor.num_telefono = request.POST['num_telefono'+id_proveedor]

        if est:
            est = get_object_or_404(
                Estados, id=request.POST['estado_proveedor'+id_proveedor])
            aux_proveedor.estado = est

        aux_proveedor.save()

        messages.success(request, 'Proveedor actualizado!!')
        return redirect(menu_proveedor)
    else:
        messages.error(request, 'Proveedor no existe!!')
        return redirect(menu_proveedor)


# -------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Cliente----------------------------------------------------------------------

@login_required
@vendedor_required
def menu_cliente(request):
    user = request.user
    client = cliente.objects.all()

    paginator = Paginator(client, 10)

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

    return render(request, 'carga_cliente.html', {"clientes": page_obj, 'user_role': user_role, 'user': user})


@login_required
@vendedor_required
def carga_cliente(request):
    est = get_object_or_404(Estados, pk=1)

    existe = cliente.objects.filter(RUC=request.POST['ruc_cliente']).exists()

    if existe:
        messages.error(request, 'El cliente ya esta cargado.')
        return redirect(menu_cliente)

    else:
        client = cliente(RUC=request.POST['ruc_cliente'], nombre=request.POST['nombre_cliente'], razon_social=request.POST['razon_social'],
                         direccion=request.POST['direccion_cliente'], correo=request.POST['correo_cliente'], estado=est, num_telefono=request.POST['num_telefono'],)
        client.save()

        messages.error(request, 'Producto guardado!!')
        return redirect(menu_cliente)


@login_required
@vendedor_required
def modificar_cliente(request):
    id_cliente = request.POST['id_cliente']

    existe = cliente.objects.filter(id=request.POST['id_cliente']).exists()

    if existe:
        est = Estados.objects.filter(
            id=request.POST['estado_cliente'+id_cliente]).exists()

        aux_cliente = get_object_or_404(cliente, pk=request.POST['id_cliente'])

        aux_cliente.RUC = request.POST['ruc_cliente'+id_cliente]
        aux_cliente.nombre = request.POST['nom_cuenta'+id_cliente]
        aux_cliente.razon_social = request.POST['razon_social'+id_cliente]
        aux_cliente.direccion = request.POST['direccion_cliente'+id_cliente]
        aux_cliente.correo = request.POST['correo_cliente'+id_cliente]
        aux_cliente.num_telefono = request.POST['num_telefono'+id_cliente]

        if est:
            est = get_object_or_404(
                Estados, id=request.POST['estado_cliente'+id_cliente])
            aux_cliente.estado = est

        aux_cliente.save()

        messages.success(request, 'Cliente actualizado!!')
        return redirect(menu_cliente)
    else:
        messages.error(request, 'Cliente no existe!!')
        return redirect(menu_cliente)
