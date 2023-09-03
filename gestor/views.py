from django.shortcuts import render,  redirect
from .models import persona

# Create your views here.
def facturas(request):
    factu = persona.objects.all()
    return render(request, 'create_factura.html', {"personas": factu })

def create_factura(request):
    factu = persona(title=request.POST['title'], description=request.POST['description'])
    factu.save()
    return redirect('/gestor/')

def delete_factura(request, factu_id):
    factu = persona.objects.get(id=factu_id)
    factu.delete()
    return redirect('/gestor/')

def ver_facturas(request):
    factu = persona.objects.all()
    return render(request, 'listar_facturas.html', {"personas": factu })