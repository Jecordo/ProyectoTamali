
from django.shortcuts import render,  redirect
from gestor.apps.usuario.models import Role, CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def cerrar_secion(request):
    logout(request)
    return redirect(menu_principal)


@login_required
def menu_principal(request):
    user = request.user
    print(user)

    if user.is_authenticated:
        try:
            custom_user = CustomUser.objects.get(user=user)
            user_role = custom_user.role.name
        except CustomUser.DoesNotExist:
            user_role = "Sin rol asignado"
    else:
        user_role = "Usuario no autenticado"

    return render(request, 'dashboard.html', {'user_role': user_role, 'user': user})
