from django.http import HttpResponse
from django.shortcuts import redirect
from gestor.apps.usuario.models import Role, CustomUser
from . import views


def is_admin(user):
    return user.role.name == 'admin'


def is_vendedor(user):
    return user.role.name == 'vendedor'


def is_contador(user):
    return user.role.name == 'contador'


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        custom_user = CustomUser.objects.get(user=request.user)
        if is_admin(custom_user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(views.menu_principal)
    return _wrapped_view


def vendedor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        custom_user = CustomUser.objects.get(user=request.user)
        if is_vendedor(custom_user) or is_admin(custom_user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(views.menu_principal)
    return _wrapped_view


def contador_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        custom_user = CustomUser.objects.get(user=request.user)
        if is_contador(custom_user) or is_admin(custom_user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(views.menu_principal)
    return _wrapped_view
