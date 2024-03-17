from datetime import date
import json
from pyexpat.errors import messages
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  redirect
from .models import cuenta, libro_diario, detalle_libro_diario
from gestor.apps.usuario.models import (Role, CustomUser)
from django.shortcuts import get_object_or_404
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


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
def mod_libro_diario(request):
    cabecera_libro = get_object_or_404(
        libro_diario, pk=request.POST['id_libro'])
    detalle_libro = detalle_libro_diario.objects.filter(
        num_asiento=cabecera_libro)
    cuentas = cuenta.objects.all()

    detalle_libro_list = [detalle.to_dict() for detalle in detalle_libro]
    detalle_libro_json = json.dumps(detalle_libro_list)

    print(detalle_libro_json)

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

'''
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
'''

@login_required
@contador_required
def llamar_funcion_django(request):
    # Realiza cualquier lógica necesaria aquí

    # Genera un enlace a la página HTML que deseas abrir en una nueva pestaña
    enlace_html = '/carga_cuenta.html'  # Reemplaza con la ruta correcta

    # Devuelve una respuesta JSON con el enlace
    return JsonResponse({'enlace_html': enlace_html})
