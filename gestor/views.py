from django.shortcuts import render,  redirect
from .models import persona, factura, factura_detalle, clientes, producto, categoria,marca,Estados,proveedor, tipo_factura, metodo_pago
from django.shortcuts import get_object_or_404


# Create your views here.
def menu_principal(request):
    return render(request, 'dashboard.html')



def facturar(request):
    prod = producto.objects.all()
    return render(request, 'create_factura.html', {"productos": prod })



def create_factura(request):
    #factu = persona(title=request.POST['title'], description=request.POST['description'])
    #factu.save()
    #return redirect('/gestor/')
    #client = get_object_or_404(clientes, pk=request.POST['cod_cateoria'])
    client = clientes.objects.filter(RUC=request.POST['ruc_cliente'])
    tip_factu = get_object_or_404(tipo_factura, pk=request.POST['tipo_factura'])
    product = get_object_or_404(producto, pk=request.POST['cod_producto'])
    est = get_object_or_404(Estados, pk=1)
    pago = get_object_or_404(metodo_pago, pk=1)


    fact = factura(cliente=client, tip_factu=tip_factu, estado=est, metodo_de_pago=pago)
    fact.save()
    
    fact_deta = factura_detalle(cod_producto=product, num_factura=fact)
    fact_deta.save()
    return redirect('/gestor/')

def delete_factura(request, factu_id):
    factu = persona.objects.get(id=factu_id)
    factu.delete()
    return redirect('/gestor/')



def ver_facturas(request):
    factu = persona.objects.all()
    return render(request, 'listar_facturas.html', {"personas": factu })


#---------------------------------------------------------------------------------------------------------------------

def menu_producto(request):
    return render(request, 'create_product.html')

def create_product(request):

    cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
    prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
    marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
    est = get_object_or_404(Estados, pk=request.POST['estado_producto'])

    produc = producto(cod_producto=request.POST['cod_producto'], precio_venta=request.POST['Precio']
                      , cod_categoria=cat, cod_proveedor=prov, cod_marca=marc, estado=est, descripcion=request.POST['desc_producto']
                      , color=request.POST['color_producto'])
    produc.save()
    return redirect('/gestor/')

def busca_producto(id_produc):
    prod = get_object_or_404(producto, pk=id_produc)
    return prod
    



def create_proveedor(request):
    return render('/gestor/')



def create_client(request):
    return render('/gestor/')



def asistencia_contable(request):
    return render('/gestor/')


