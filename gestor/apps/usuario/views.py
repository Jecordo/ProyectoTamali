
from pyexpat.errors import messages
from django.shortcuts import render,  redirect
from gestor.apps.usuario.models import (Role, CustomUser)
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from gestor.decorators import admin_required

@login_required
def cerrar_secion(request):
    request.session.pop('rol', None)

    logout(request)
    return redirect(menu_principal)


@never_cache
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

    request.session['rol'] = user_role

    return render(request, 'dashboard.html', {'user': user})


@login_required
@admin_required
def crear_user(request):
    user_actua = request.user
    rol = Role.objects.all()

    if user_actua.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user_actua)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    if request.method == 'GET':
        return render(request, 'crear_user.html', {'user_role': user_role, 'user': user_actua, 'rols': rol})

    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        email = request.POST.get('email', '')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El usuario ya existe.')
            else:
                user = User.objects.create_user(
                    username=username, password=password1)

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
def modificar_user(request):
    user = request.user

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    usuario = get_object_or_404(CustomUser, pk=request.POST['id_usuario'])
    return render(request, 'modificar_user.html', {'user_role': user_role, 'user': user, 'usuario': usuario})


@login_required
@admin_required
def modificar_user_final(request):
    print(request.POST['id_user'])

    id_user = request.POST['id_user']
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    nombre = request.POST.get('nombre', '')
    apellido = request.POST.get('apellido', '')
    email = request.POST.get('email', '')

    if password1 == password2:
        if User.objects.filter(id=id_user).exists():
            user_aux = User.objects.filter(id=id_user).first()
            role = Role.objects.get(name=request.POST['rols'])

            custom_user = get_object_or_404(CustomUser, user=user_aux)

            user_aux.username = username
            user_aux.save()

            custom_user.role = role
            custom_user.nombre = nombre
            custom_user.apellido = apellido
            custom_user.email = email
            custom_user.save()

            messages.success(request, 'Usuario actualizado.')
        else:

            messages.error(request, 'El usuario no existe.')

    else:
        messages.error(request, 'Las contraseñas no coinciden.')

    return redirect(listar_user)


@login_required
@admin_required
def eliminar_user(request):
    user_aux = get_object_or_404(CustomUser, pk=request.POST['id_usuario'])
    usuario = get_object_or_404(User, id=user_aux.user.id)
    user = request.user

    if user == usuario:
        messages.error(request, 'No se puede eliminar usuario logeado.')
    else:
        usuario.delete()
        user_aux.delete()

    return redirect(listar_user)


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
