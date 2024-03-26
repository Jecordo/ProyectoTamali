from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyexpat.errors import messages
import re
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  redirect
from gestor.apps.factura.models import (
    factura, factura_detalle, metodo_pago, tipo_factura, detalle_temp)
from gestor.apps.cliente.models import cliente
from gestor.apps.producto.models import producto
from gestor.apps.estado.models import estado as Estados
from gestor.apps.inventario.models import inventario, stock
from gestor.apps.usuario.models import CustomUser, Role
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestor.decorators import vendedor_required


# -----------------------------------Factura----------------------------------------------
# ----------------------------------------------------------------------------------------


@login_required
@vendedor_required
def facturar(request):
    request.session.pop('factura_cabecera_id', None)

    user = request.user
    client = cliente.objects.all()
    metodo = metodo_pago.objects.all()
    tipo = tipo_factura.objects.all()
    factu_prduc = []

    ultimoa_factura = factura.objects.all().exists()

    if ultimoa_factura:
        ultimoa_factura = factura.objects.order_by('-num_factura').first()
        timbrado = ultimoa_factura.timbrado
        fecha_fact = ultimoa_factura.fecha
        num_factura = int(ultimoa_factura.num_factura[-7:]) + 1
        num_factura = f"{num_factura:07d}"
    else:
        timbrado = 00000000
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

    return render(request, 'Factura/create_factura.html', {"clientes": client, "ultima_factura": num_factura, "timbrado": timbrado,
                                                   "factu_prduc": factu_prduc, "metodos_pagos": metodo,
                                                   'tipos_facturas': tipo, 'user_role': user_role})


@login_required
@vendedor_required
def create_factura(request):
    num_factura = request.POST['num_factura']
    ultimo_numero_factura = num_factura.split('-')[-1]
    existe = factura.objects.filter(num_factura=ultimo_numero_factura).exists()

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
    
    num_factura = request.POST['num_factura']
    ultimo_numero_factura = num_factura.split('-')[-1]

    factura_cabecera = factura(fecha=request.POST['fecha_emision'], num_factura=ultimo_numero_factura, cliente=client, tipo_factura=factura_tipo,
                               metodo_de_pago=ment_pag, estado=est, timbrado=request.POST['timbrado_factura'])
    factura_cabecera.save()

    factura_cabecera_id = factura_cabecera.id
    request.session['factura_cabecera_id'] = factura_cabecera_id

    return redirect(menu_factura_detalle)


#------------------------------------imprimir facturas-----------------------------------------------
def imprimir_factura(request):
    id_factura = request.POST['id_factura']
    facturas = get_object_or_404(factura, pk=id_factura)  # Recupera la factura por su ID o cualquier otro criterio
    detalles_factura = factura_detalle.objects.filter(num_factura=facturas)

    # Crear el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    # Datos del cliente
    p.drawString(100, 750, f'{facturas.cliente.razon_social}')
    p.drawString(100, 735, f'{facturas.cliente.RUC}')
    p.drawString(100, 720, f'{facturas.cliente.direccion}')
    p.drawString(100, 705, f'{facturas.cliente.num_telefono}')

    # Agregar contenido al PDF
    p.drawString(450, 750, f'{facturas.num_factura}')
    p.drawString(450, 730, f'{facturas.fecha.strftime("%d/%m/%Y")}')
    p.drawString(450, 710, f'{facturas.cliente}')
    p.drawString(50, 690, 'Detalles de la factura:')
    y = 670  # Posición vertical para los detalles

    aux = 0

    if not detalles_factura:
        print('No entro')
    else:
        for detalle in detalles_factura:
            p.drawString(50, y+aux, f'{detalle.cod_producto}')
            p.drawString(100, y+aux, f'{detalle.cod_producto.descripcion}')
            p.drawString(300, y+aux, f'{detalle.cantidad}')
            p.drawString(350, y+aux, f'{detalle.descuento}%')
            p.drawString(380, y+aux, f'{detalle.cod_producto.precio_venta}')
            p.drawString(430, y+aux, f'{detalle.total_precio}')
            aux -= 10       
        p.drawString(440, 490, f'{detalle.impuesto}')
        p.drawString(440, 480, f'{detalle.total_precio}')

    # --------------------------- Copia de la factura ------------------------------------------------------

    p.drawString(100, 400, f'{facturas.cliente.razon_social}')
    p.drawString(100, 375, f'{facturas.cliente.RUC}')
    p.drawString(100, 360, f'{facturas.cliente.direccion}')
    p.drawString(100, 345, f'{facturas.cliente.num_telefono}')

    # Agregar contenido al PDF
    p.drawString(450, 400, f'{facturas.num_factura}')
    p.drawString(450, 380, f'{facturas.fecha.strftime("%d/%m/%Y")}')
    p.drawString(450, 360, f'{facturas.cliente}')
    p.drawString(50, 340, 'Detalles de la factura:')
    y = 320  # Posición vertical para los detalles

    aux = 0

    if not detalles_factura:
        print('No entro')
    else:
        for detalle in detalles_factura:
            p.drawString(50, y+aux, f'{detalle.cod_producto}')
            p.drawString(100, y+aux, f'{detalle.cod_producto.descripcion}')
            p.drawString(300, y+aux, f'{detalle.cantidad}')
            p.drawString(350, y+aux, f'{detalle.descuento}%')
            p.drawString(380, y+aux, f'{detalle.cod_producto.precio_venta}')
            p.drawString(430, y+aux, f'{detalle.total_precio}')
            aux -= 10       
        p.drawString(440, 140, f'{detalle.impuesto}')
        p.drawString(440, 150, f'{detalle.total_precio}')

    # --------------- Anulacion de factura ----------------------

    if facturas.estado.estado == 'Inactivo':
        p.rotate(35)
        p.setFont("Helvetica-Bold", 60)  # Tamaño de fuente grande y negrita
        p.setFillColorRGB(1, 0, 0)
        p.drawString(450, 300, "ANULADO")
        p.drawString(250, 10, "ANULADO")
        p.rotate(-35)

    # Cierra el PDF y envía la respuesta
    p.showPage()
    p.save()
    return response


# -----------------------------------Detalle de la factura----------------------------------------------


@login_required
@vendedor_required
def menu_factura_detalle(request):
    factura_cabecera_id = request.session.get('factura_cabecera_id')
    user = request.user

    productos = stock.objects.exclude(cantidad='0')
    factura_cabecera = get_object_or_404(factura, pk=factura_cabecera_id)

    factu_detalle = detalle_temp.objects.filter(
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

    return render(request, 'Factura/create_factura_detalle.html', {"factura_cabecera": factura_cabecera, "productos": productos,
                                                           "facturas_detalles": factu_detalle, "total_compra": suma, "total_iva": suma_iva,
                                                           'user_role': user_role, 'user': user})


@login_required
@vendedor_required
def cargar_factura_detalle(request):

    num_factura = request.POST['num_factura']
    ultimo_numero_factura = num_factura.split('-')[-1]

    factu = get_object_or_404(factura, num_factura=ultimo_numero_factura)
    produc = get_object_or_404(
        producto, pk=int(request.POST['cod_producto_id']))

    existe = detalle_temp.objects.filter(
        cod_producto=produc.id, num_factura=factu.id).exists()

    if existe:
        messages.success(request,  produc.descripcion +
                         ', ya se encuentra agregado')
    else:
        factu_detalle = detalle_temp(cod_producto=produc, num_factura=factu, total_precio=produc.precio_venta,
                                     cantidad=1, impuesto=produc.iva_producto, descuento=0)

        factu_detalle.save()

        messages.success(request, 'Se agrego '+produc.descripcion)

    return redirect(menu_factura_detalle)


@login_required
@vendedor_required
def finalizar_factura(request):
    fecha_hoy = date.today()
    factura_cabecera_id = request.session.get('factura_cabecera_id')
    request.session.pop('factura_cabecera_id', None)

    cantidad_str = request.POST.get('cant_prod', '')
    descuento_str = request.POST.get('desc_prod', '')
    iva_str = request.POST.get('iva_prod', '')

    cantidad_lista = cantidad_str.split(",") 
    print(cantidad_lista)
    descuento_lista = descuento_str.split(",")
    iva_lista = iva_str.split(",")

    factu = get_object_or_404(factura, pk=factura_cabecera_id)
    existe = detalle_temp.objects.all().exists()

    if existe:
        factu_detall = detalle_temp.objects.all()
        total_iva = 0
        total_precios = 0
        i = 1

        for pro in (factu_detall):
            if cantidad_lista[i] == "":
                cantidad = 0
            else:
                cantidad = int(cantidad_lista[i])

            iva = float(iva_lista[i])
            descuento = int(descuento_lista[i])

            stocks = stock.objects.filter(producto=pro.cod_producto.id).first()
            if cantidad > int(stocks.cantidad):
                print('entro')
                request.session['factura_cabecera_id'] = factura_cabecera_id

                messages.error(
                    request, 'El producto '+str(pro.cod_producto.cod_producto)+' supera la cantidad de stock, se cuenta con '+str(stocks.cantidad))
                return redirect(menu_factura_detalle)
            elif str(cantidad) == '0':
                print('entro en nulo')
                request.session['factura_cabecera_id'] = factura_cabecera_id

                messages.error(
                    request, 'El producto '+str(pro.cod_producto.cod_producto)+' no puede tener cantidad nula o valor 0')
                return redirect(menu_factura_detalle)
            else:
                print('no entrro')

            descuento_pro = (
                (pro.cod_producto.precio_venta*descuento)/100)*cantidad

            total_precio = (
                pro.cod_producto.precio_venta*cantidad) - descuento_pro

            factu_detalle = factura_detalle(cod_producto=pro.cod_producto, num_factura=factu, total_precio=total_precio,
                                            cantidad=cantidad, impuesto=iva, descuento=descuento_pro)
            factu_detalle.save()

            total_iva = total_iva + iva
            total_precios = total_precios + pro.total_precio

            inv = inventario(fecha=fecha_hoy, cod_producto=pro.cod_producto, descripcion='Venta',
                             tipo_movimiento=False, cantidad=cantidad, referencia=factu.num_factura)
            inv.save()

            i += 1

        factu_detall = detalle_temp.objects.all()
        factu_detall.delete()

        factu.total_venta = total_precios
        factu.impuesto_total = total_iva
        factu.save()

        factura_cabecera_id = int(factu.id)
        return redirect(listar_factura)
    else:
        factu.delete()

        messages.error(request, 'No se facturo, factura vacia')

        return redirect(facturar)
    

@login_required
@vendedor_required
def listar_factura(request):
    factu = factura.objects.all().order_by('num_factura')
    user = request.user
    print(user)


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

    tipo = tipo_factura.objects.all()

    # Filtrar los productos

    if 'categoria_filter' in request.POST and request.POST['categoria_filter'] != '':
        factu = factu.filter(
            tipo_factura=request.POST['categoria_filter'])

    if 'nombre_filter' in request.POST and request.POST['nombre_filter'] != '':
        factu = factu.filter(
            num_factura__icontains=request.POST['nombre_filter'])

    paginator = Paginator(factu, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Factura/listar_factura.html', {"facturas": page_obj, "user_role": user_role, 'user': user,
                                               "tipos_facturas": tipo})

@login_required
@vendedor_required
def delete_factura(request):
    prod = stock.objects.exclude(cantidad=0)
    for p in prod:
        print(p.producto, p.cantidad)
    factu_detalle = get_object_or_404(
        detalle_temp, pk=int(request.POST['id_detalle']))
    num_factura = factu_detalle.num_factura
    factu_detalle.delete()

    factu_detalles = detalle_temp.objects.filter(
        num_factura=num_factura).order_by('id')

    suma = 0
    for precio in factu_detalles:
        suma = suma + precio.total_precio

    factu_cabecera = get_object_or_404(factura, num_factura=num_factura)

    return render(request, 'Factura/create_factura_detalle.html', {"factura_cabecera": factu_cabecera, "productos": prod,
                                                           "facturas_detalles": factu_detalles, "total_compra": suma})

@login_required
@vendedor_required
def cancelar_factura(request, factura_cabecera_id):

    factura_cabecera = get_object_or_404(factura, pk=factura_cabecera_id)
    factu_detalle = detalle_temp.objects.filter(
        num_factura=factura_cabecera.id).order_by('id')
    factu_detalle.delete()
    factura_cabecera.delete()

    return redirect(facturar)


# ------------------------------------ Anular factura ---------------------------------------

@login_required
@vendedor_required
def anular_factura(request, factura_id):
    factura_obj = get_object_or_404(factura, id=factura_id)
    
    if factura_obj.estado == 'Anulada':
        return redirect(listar_factura)
    
    estado_asignado = get_object_or_404(Estados, id=2)
    factura_obj.estado = estado_asignado
    factura_obj.save()
    
    return redirect(listar_factura)