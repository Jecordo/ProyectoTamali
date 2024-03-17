
from pyexpat.errors import messages
from django.shortcuts import render,  redirect
from .models import (cliente)
from gestor.apps.estado.models import estado as Estados
from gestor.apps.usuario.models import (Role, CustomUser)
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestor.decorators import vendedor_required


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

        messages.success(request, 'Cliente guardado!!')
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
