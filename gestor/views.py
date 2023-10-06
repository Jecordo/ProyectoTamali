from datetime import date
from io import BytesIO
import json
from pyexpat.errors import messages
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  redirect
from .models import (
    persona, factura, factura_detalle, clientes, producto,
    categoria,marca,Estados,proveedor, tipo_factura, 
    metodo_pago, marca, cuenta, libro_diario, libro_mayor)
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




# Create your views here.
def menu_principal(request):
    return render(request, 'dashboard.html')



def facturar(request):
    client = clientes.objects.all()
    factu_prduc = []

    ultimoa_factura = factura.objects.order_by('-num_factura').first()
    
    if ultimoa_factura is not None and ultimoa_factura.num_factura:
        num_factura = int(ultimoa_factura.num_factura) + 1
        num_factura = f"{num_factura:07d}" 

    else:
        num_factura = 1  # Si no hay facturas o la última factura no tiene un número válido, comenzamos desde 1

    return render(request, 'create_factura.html', {"clientes": client, "ultima_factura": num_factura, "factu_prduc":factu_prduc})



def create_factura(request):
    #factu.save()
    #return redirect('/gestor/')
    #client = get_object_or_404(clientes, pk=request.POST['cod_cateoria'])
    print(request.POST.get('ruc_cliente', '') ) # Obtener el RUC del formulario)
    print(request.POST.get('razon_social', '') ) # Obtener el RUC del formulario)

    return redirect(facturar)

#def busca_producto(request):
 #   objeto_lista = request.POST.getlist('factu[]')
  #  return


def busca_producto(request):
    if request.method == 'POST':
        objetos_json = request.POST.get('objetos')
        objetos = json.loads(objetos_json)

        # Realiza alguna operación con la lista de objetos
        for objeto in objetos:
            # Hacer algo con cada objeto, como guardarlo en una base de datos
            pass

        return JsonResponse({'message': 'Lista de objetos procesada con éxito'})
    else:
        return JsonResponse({'message': 'Solicitud no válida'}, status=400)


def obtener_productos(request, cod_producto):
    productos = producto.objects.filter(num_producto=cod_producto)
    productos_data = []
    for prod in productos:
        productos_data.append({
            'cod_producto': prod.cod_producto,
            'descripcion': prod.descripcion,
            # Agrega más campos según tus necesidades
        })
    return JsonResponse({'productos': productos})


def delete_factura(request, factu_id):
    factu = persona.objects.get(id=factu_id)
    factu.delete()
    return redirect('/gestor/')



def ver_facturas(request):
    factu = persona.objects.all()
    return render(request, 'listar_facturas.html', {"personas": factu })


#---------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Producto----------------------------------------------------------------------

def menu_producto(request):
    marc = marca.objects.all()
    catg = categoria.objects.all()
    prov = proveedor.objects.all()

    return render(request, 'create_product.html', {"marcas": marc, "categorias": catg, 
                                                   "proveedores": prov})

def create_product(request):
    marcas = marca.objects.all()
    catgedorias = categoria.objects.all()
    proveedores = proveedor.objects.all()
    estados = Estados.objects.all()    

    existe = producto.objects.filter(cod_producto=request.POST['cod_producto']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})

    else:
        cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
        prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
        marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
        est = get_object_or_404(Estados, pk=1)

        produc = producto(cod_producto=request.POST['cod_producto'], precio_costo=request.POST['precio_compra']
                          ,precio_venta=request.POST['precio_venta'], cod_categoria=cat, cod_proveedor=prov, cod_marca=marc, estado=est
                          ,descripcion=request.POST['desc_producto'])
        produc.save()

        mensaje_error = "Producto guardado!!"
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})


    
def buscar_producto(request):
    objetos = producto.objects.all().values_list('cod_producto', flat=True)
    return JsonResponse(list(objetos), safe=False)

#-------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Libro diario----------------------------------------------------------------------
@never_cache
def menu_libro_diario(request):
    fecha_hoy = date.today()

    libros_diarios = libro_diario.objects.filter(fecha__year=fecha_hoy.year).order_by('fecha', 'num_asiento','id')
    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_diarios, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cargar_asiento_diario.html', {"libros_diarios": page_obj, "cuentas": cuentas})

@never_cache
def cargar_libro_diario(request):
    aux_lib = libro_diario.objects.order_by('-id').first()
    cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'])
    tipo_mov = request.POST['tipo_movimiento']

    if aux_lib and aux_lib.num_asiento != int(request.POST['num_asiento']):
        corroboration = libro_diario.objects.filter(num_asiento=aux_lib.num_asiento)
        suma=0

        for lib in corroboration:
            suma = suma + lib.debe
            suma = suma - lib.haber

        if suma != 0:
            messages.error(request, 'El asiento no está equilibrado.')
            return redirect(menu_libro_diario)

    if tipo_mov == "1":

        libro = libro_diario(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                        ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=request.POST['id_monto'], haber=0)

        libro.save()
        
    elif tipo_mov == "2":

        libro = libro_diario(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                        ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=0, haber=request.POST['id_monto'])

        libro.save()

    messages.success(request, 'Asiento guardado!!')
    return redirect(menu_libro_diario)

@never_cache
def modificar_libro_diario(request):
    fecha_actual = date.today()

    libros_diarios = libro_diario.objects.filter(fecha__year=fecha_actual.year).order_by('fecha', 'num_asiento')
    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_diarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    existe = libro_diario.objects.filter(id=request.POST['id_libro']).exists()

    if existe:
        aux = request.POST['id_libro']
        aux_libro = get_object_or_404(libro_diario, pk=request.POST['id_libro'])
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'+aux])

        aux_libro.fecha = request.POST['fecha_emision'+aux]
        aux_libro.num_asiento = request.POST['num_asiento'+aux]
        aux_libro.concepto = request.POST['id_concepto'+aux]
        aux_libro.num_cuenta = cta
        aux_libro.haber = request.POST['monto_haber'+aux]
        aux_libro.debe = request.POST['monto_debe'+aux]
        
        aux_libro.save()

        mensaje_error = "Asiento actualizado!!"
        return redirect(menu_libro_diario)
    else:
        mensaje_error = "Asiento no esta cargado."

        return render(request, 'cargar_asiento_diario.html', {"libros_diarios": page_obj, "cuentas": cuentas, "mensaje_error": mensaje_error})


@never_cache
def descargar_libro(request):
    fecha_libro = request.POST['fecha_deseada']

    if re.match(r'^\d{4}-(0[1-9]|1[0-2])$', fecha_libro):
        year, month = map(int, fecha_libro.split('-'))

        datos = libro_diario.objects.filter(Q(fecha__year=year) & Q(fecha__month=month)).order_by('fecha', 'num_asiento')

    else:
        year = int(fecha_libro)
        print(year)

        datos = libro_diario.objects.filter(fecha__year=year).order_by('fecha', 'num_asiento')

    df = pd.DataFrame(list(datos.values('fecha', 'num_asiento', 'concepto', 'num_cuenta', 'debe', 'haber')))

    libro_excel = Workbook()

    hoja = libro_excel.active

    for fila in dataframe_to_rows(df, index=False, header=True):
        hoja.append(fila)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libro diario.xlsx'

    libro_excel.save(response)

    return response

def migrar_asientos(request):
    asientos_migrar = libro_diario.objects.all().order_by('num_asiento')
    libros_mayores = libro_mayor.objects.all().order_by('num_asiento')

    if asientos_migrar.count()==libros_mayores.count():
        return redirect(menu_libro_mayor)

    else:
        for asiento in asientos_migrar[libros_mayores.count():]:
            libro_mayor_mas_reciente = libro_mayor.objects.filter(num_cuenta=asiento.num_cuenta).order_by('-id').first()

            if libro_mayor_mas_reciente:
                saldo = libro_mayor_mas_reciente.saldo + asiento.debe
                saldo = saldo - asiento.haber
                num_asiento = int(libro_mayor_mas_reciente.num_asiento)+1
            else:
                saldo = asiento.debe
                saldo = saldo - asiento.haber
                num_asiento = 1

            libro = libro_mayor(fecha=asiento.fecha, num_asiento=num_asiento,concepto=asiento.concepto, 
                                num_cuenta=asiento.num_cuenta, debe=asiento.debe, haber=asiento.haber, saldo=saldo)

            libro.save()


        messages.success(request, 'Asiento guardado!!')
        return redirect(menu_libro_mayor)


#-------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Libro mayor----------------------------------------------------------------------

@never_cache
def menu_libro_mayor(request):
    fecha_hoy = date.today()

    if 'num_cuenta' in request.POST:
        libros_mayores = libro_mayor.objects.filter(num_cuenta=request.POST['num_cuenta'], fecha__year=fecha_hoy.year).order_by('num_asiento', 'num_cuenta')
    else:
        lib = libro_mayor.objects.order_by('-fecha').first()
        libros_mayores = libro_mayor.objects.filter(num_cuenta=lib.num_cuenta).order_by('num_asiento', 'num_cuenta')

    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_mayores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cargar_asiento_mayor.html', {
        "libros_mayores": page_obj,
        "cuentas": cuentas,
    })

@never_cache
def cargar_libro_mayor(request):
    fecha_hoy = date.today()

    libros_mayores = libro_mayor.objects.filter(fecha__year=fecha_hoy.year).order_by('fecha', 'num_asiento')
    cuentas = cuenta.objects.all()

    paginator = Paginator(libros_mayores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    existe = libro_mayor.objects.filter(num_asiento=request.POST['num_asiento'], num_cuenta=request.POST['num_cuenta']).exists()

    if existe:
        return redirect(menu_libro_mayor)
    
    else:
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'])
        libro_mayor_mas_reciente = libro_mayor.objects.order_by('-fecha').first()
        tipo_mov = request.POST['tipo_movimiento']

        if libro_mayor_mas_reciente:
            saldo = libro_mayor_mas_reciente.saldo + int(request.POST['id_monto'])
        else:
            saldo = int(request.POST['id_monto'])

        if tipo_mov == "1":

            libro = libro_mayor(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                            ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=request.POST['id_monto'], haber=0, saldo=saldo)

            libro.save()
            
        elif tipo_mov == "2":

            libro = libro_mayor(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                            ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=0, haber=request.POST['id_monto'], saldo=saldo)

            libro.save()

        messages.success(request, 'Asiento guardado!!')
        return redirect(menu_libro_mayor)



@never_cache
def modificar_libro_mayor(request):
    id_libro = request.POST['id_libro']
    cont=0

    libros_mayores = libro_mayor.objects.filter(pk__gte=id_libro).order_by('num_asiento')

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
            saldo_agregado = saldo_agregado - int(request.POST['monto_haber'+id_libro])

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
                cont+=1
        
        messages.success(request, 'Asiento actualizado!!')
        return redirect(menu_libro_mayor)
    else:
        messages.success(request, 'Asiento no esta cargado.')

        return redirect(menu_libro_mayor)
    
def obtener_libro_mayor_anterior(id_libro):
    try:
        libro_mayor_anterior = libro_mayor.objects.filter(pk__lt=id_libro).latest('pk')
        return libro_mayor_anterior
    except libro_mayor.DoesNotExist:
        return None

@never_cache
def descargar_libro_mayor(request):
    fecha_libro = request.POST['fecha_libro']

    if re.match(r'^\d{4}-(0[1-9]|1[0-2])$', fecha_libro):
        year, month = map(int, fecha_libro.split('-'))

        datos = libro_diario.objects.filter(Q(fecha__year=year) & Q(fecha__month=month)).order_by('fecha', 'num_asiento')

    else:
        year = int(fecha_libro)
        month = 1

        datos = libro_diario.objects.all().order_by('fecha', 'num_asiento')



    df = pd.DataFrame(list(datos.values('fecha', 'num_asiento', 'concepto', 'num_cuenta', 'debe', 'haber')))

    libro_excel = Workbook()

    hoja = libro_excel.active

    for fila in dataframe_to_rows(df, index=False, header=True):
        hoja.append(fila)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libro diario.xlsx'

    libro_excel.save(response)

    return response
#----------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Cuentas----------------------------------------------------------------------

@never_cache
def menu_cuenta(request):
    cuentas = cuenta.objects.all().order_by('id')

    paginator = Paginator(cuentas, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'carga_cuenta.html', {"cuentas": page_obj})

@never_cache
def registrar_cuenta(request):

    existe = cuenta.objects.filter(num_cuenta=request.POST['num_cuenta']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return redirect(menu_cuenta)

    else:

        cta = cuenta(num_cuenta=request.POST['num_cuenta'], descripcion=request.POST['nom_cuenta'], saldo=request.POST['id_monto'])
        cta.save()

        mensaje_error = "Producto guardado!!"
        return redirect(menu_cuenta)

@never_cache
def modificar_cuenta(request):
    id_cuenta = request.POST['id_cuenta']

    existe = cuenta.objects.filter(id=request.POST['id_cuenta']).exists()

    if existe:
        aux_cuenta= get_object_or_404(cuenta, pk=request.POST['id_cuenta'])

        aux_cuenta.num_cuenta = request.POST['num_cuenta'+id_cuenta]
        aux_cuenta.descripcion = request.POST['nom_cuenta'+id_cuenta]
        aux_cuenta.saldo = request.POST['id_monto'+id_cuenta]

        aux_cuenta.save()

        mensaje_error = "Asiento actualizado!!"
        return redirect(menu_cuenta)
    else:
        mensaje_error = "Asiento no esta cargado."

        return redirect(menu_cuenta)

#-------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Proveedor----------------------------------------------------------------------

def create_proveedor(request):
    return render('/gestor/')



def create_client(request):
    return render('/gestor/')



def asistencia_contable(request):
    return render('/gestor/')


