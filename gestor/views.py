from django.shortcuts import render,  redirect
from .models import persona

# Create your views here.
def facturas(request):
    factu = persona.objects.all()
    return render(request, 'facturas.html', {"personas": factu })

def create_factura(request):
    factu = persona(title=request.POST['title'], description=request.POST['description'])
    factu.save()
    return redirect('/gestor/')