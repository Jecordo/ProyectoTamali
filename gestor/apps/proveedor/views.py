
from pyexpat.errors import messages
from django.shortcuts import render,  redirect
from .models import proveedor
from gestor.apps.estado.models import estado as Estados
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, Page
from django.contrib import messages
from gestor.apps.usuario.models import Role, CustomUser
from django.contrib.auth.decorators import login_required
from gestor.decorators import admin_required, vendedor_required, contador_required


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
