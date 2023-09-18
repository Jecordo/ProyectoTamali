from django.http import JsonResponse
from django.shortcuts import render,  redirect
from .models import persona, factura, factura_detalle, clientes, producto, categoria,marca,Estados,proveedor, tipo_factura, metodo_pago, marca
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

    if request.method == 'POST':
        ruc_cliente = request.POST.get('ruc_cliente', '')  # Obtener el RUC del formulario

        # Intentar obtener el cliente por su RUC
        try:
            client = clientes.objects.get(RUC=ruc_cliente)
        except clientes.DoesNotExist:
            # El cliente no existe en la base de datos, puedes manejar esto como desees,
            # por ejemplo, mostrar un mensaje de error.
            return redirect('/gestor/')


    #client = clientes.objects.get(RUC=request.POST['ruc_cliente'])
    print(client)
    tip_factu = get_object_or_404(tipo_factura, pk=request.POST['tipo_factura'])
    product = get_object_or_404(producto, pk=request.POST['cod_producto'])
    est = get_object_or_404(Estados, pk=1)
    pago = get_object_or_404(metodo_pago, pk=1)


    fact = factura(cliente=client, tipo_factura=tip_factu, estado=est, metodo_de_pago=pago, total_venta=request.POST['precio'])
    fact.save()
    
    fact_deta = factura_detalle(cod_producto=product, num_factura=fact, precio_unitario=request.POST['precio'])
    fact_deta.save()
    return redirect('/gestor/facturar/')

def delete_factura(request, factu_id):
    factu = persona.objects.get(id=factu_id)
    factu.delete()
    return redirect('/gestor/')



def ver_facturas(request):
    factu = persona.objects.all()
    return render(request, 'listar_facturas.html', {"personas": factu })


#---------------------------------------------------------------------------------------------------------------------

def menu_producto(request):
    marc = marca.objects.all()
    catg = categoria.objects.all()
    prov = proveedor.objects.all()

    return render(request, 'create_product.html', {"marcas": marc, "categorias": catg, 
                                                   "proveedores": prov})

def create_product(request):

    print(request.POST['cod_cateoria'])
    cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
    prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
    marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
    est = get_object_or_404(Estados, pk=request.POST['1'])

    produc = producto(cod_producto=request.POST['cod_producto'], precio_venta=request.POST['precio_venta']
                      , precio_costo=request.POST['precio_compra'], cod_categoria=cat, cod_proveedor=prov
                      , cod_marca=marc, estado=est, descripcion=request.POST['desc_producto'])
    produc.save()
    return redirect('/gestor/')

#def busca_producto(id_produc):
#    prod = get_object_or_404(producto, pk=id_produc)
#    return prod
    
def buscar_producto(request):
    codigo_producto = request.GET.get('codigo', '')
    try:
        produc = producto.objects.get(cod_producto=codigo_producto)
        # Si se encuentra el producto, puedes devolver sus detalles en la respuesta JSON
        response_data = {
            'success': True,
            'produc': {
                'descripcion': produc.descripcion,
                # Agrega otros campos del producto que desees enviar
            }
        }
    except produc.DoesNotExist:
        response_data = {'success': False}

    return JsonResponse(response_data)

#-------------------------------------------------------------------------------------------------------------------------

def create_proveedor(request):
    return render('/gestor/')



def create_client(request):
    return render('/gestor/')



def asistencia_contable(request):
    return render('/gestor/')


