from datetime import date
from pyexpat.errors import messages
from django.shortcuts import render,  redirect
from .models import (cuenta)
from gestor.apps.usuario.models import (Role, CustomUser)
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, Page
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


# ----------------------------------------------------------------------------------------------------------------------
#  ---------------------------------Cuentas----------------------------------------------------------------------

@never_cache
@login_required
@contador_required
def menu_cuenta(request):
    user = request.user
    cuentas = cuenta.objects.all().order_by('id')

    paginator = Paginator(cuentas, 10)

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

    if existe:
        messages.error(request, 'Cuenta ya existe!!')
        return redirect(menu_cuenta)

    else:
        cta = cuenta(num_cuenta=request.POST['num_cuenta'],
                     descripcion=request.POST['nom_cuenta'], saldo=0)
        cta.save()

        messages.success(request, 'Cuenta guardada!!')
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
