from datetime import date
from pyexpat.errors import messages
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  redirect
from .models import (cuenta, libro_mayor)
from gestor.apps.usuario.models import (Role, CustomUser)
from django.shortcuts import get_object_or_404
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


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