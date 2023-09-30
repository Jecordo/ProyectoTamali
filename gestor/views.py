from datetime import date
import json
from django.http import JsonResponse
from django.shortcuts import render,  redirect
from .models import (
    persona, factura, factura_detalle, clientes, producto,
    categoria,marca,Estados,proveedor, tipo_factura, 
    metodo_pago, marca, cuenta, libro_diario, libro_mayor)
from django.shortcuts import get_object_or_404


# Create your views here.
def menu_principal(request):
    return render(request, 'dashboard.html')



def facturar(request):
    prod = producto.objects.all()
    factu_prduc = []

    ultimoa_factura = factura.objects.order_by('-num_factura').first()
    
    if ultimoa_factura is not None and ultimoa_factura.num_factura:
        num_factura = int(ultimoa_factura.num_factura) + 1
        num_factura = f"{num_factura:07d}" 

    else:
        num_factura = 1  # Si no hay facturas o la última factura no tiene un número válido, comenzamos desde 1

    print(num_factura)

    return render(request, 'create_factura.html', {"productos": prod, "ultima_factura": num_factura, "factu_prduc":factu_prduc})



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

#def busca_producto(request):
 #   objeto_lista = request.POST.getlist('factu[]')
  #  return


def busca_producto(request):
    if request.method == 'POST':
        objetos_json = request.POST.get('objetos')
        objetos = json.loads(objetos_json)

        # Realiza alguna operación con la lista de objetos
        for objeto in objetos:
            # Hacer algo con cada objeto, como guardarlo en una base de datos
            pass

        return JsonResponse({'message': 'Lista de objetos procesada con éxito'})
    else:
        return JsonResponse({'message': 'Solicitud no válida'}, status=400)


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
    marcas = marca.objects.all()
    catgedorias = categoria.objects.all()
    proveedores = proveedor.objects.all()
    estados = Estados.objects.all()    

    existe = producto.objects.filter(cod_producto=request.POST['cod_producto']).exists()

    if existe:
        mensaje_error = "Producto ya existe."
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})

    else:
        cat = get_object_or_404(categoria, pk=request.POST['cod_cateoria'])
        prov = get_object_or_404(proveedor, pk=request.POST['prov_producto'])
        marc = get_object_or_404(marca, pk=request.POST['marca_producto'])
        est = get_object_or_404(Estados, pk=1)

        produc = producto(cod_producto=request.POST['cod_producto'], precio_costo=request.POST['precio_compra']
                          ,precio_venta=request.POST['precio_venta'], cod_categoria=cat, cod_proveedor=prov, cod_marca=marc, estado=est
                          ,descripcion=request.POST['desc_producto'])
        produc.save()

        mensaje_error = "Producto guardado!!"
        return render(request, 'create_product.html', {'mensaje_error': mensaje_error, "marcas": marcas, "categorias": catgedorias, "proveedores": proveedores, "estados": estados})


    
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

def menu_libro_diario(request):
    fecha_actual = date.today()
    libros_diarios = libro_diario.objects.filter(fecha=fecha_actual)
    cuentas = cuenta.objects.all()

    return render(request, 'cargar_asiento_diario.html', {"libros_diarios": libros_diarios, "cuentas": cuentas})


def cargar_libro_diario(request):
    fecha_actual = date.today()
    libros_diarios = libro_diario.objects.filter(fecha=fecha_actual)
    cuentas = cuenta.objects.all()

    existe = libro_diario.objects.filter(num_asiento=request.POST['num_asiento']).exists()

    if existe:
        mensaje_error = "Asiento ya existe."

        return render(request, 'cargar_asiento_diario.html', {"libros_diarios": libros_diarios, "cuentas": cuentas, "mensaje_error":mensaje_error})

    else:
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'])
        tipo_mov = request.POST['tipo_movimiento']

        if tipo_mov == "1":

            libro = libro_diario(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                            ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=request.POST['id_monto'], haber=0)

            libro.save()
            
        elif tipo_mov == "2":

            libro = libro_diario(fecha=request.POST['fecha_emision'], num_asiento=request.POST['num_asiento']
                            ,concepto=request.POST['id_concepto'], num_cuenta=cta, debe=0, haber=request.POST['id_monto'])

            libro.save()

        mensaje_error = "Asiento guardado!!"
        return render(request, 'cargar_asiento_diario.html', {"libros_diarios": libros_diarios, "cuentas": cuentas, "mensaje_error": mensaje_error})



def modificar_libro_diario(request):
    fecha_actual = date.today()
    libros_diarios = libro_diario.objects.filter(fecha=fecha_actual)
    cuentas = cuenta.objects.all()

    existe = libro_diario.objects.filter(num_asiento=request.POST['num_asiento']).exists()

    if existe:
        aux_libro = libro_diario.objects.get( num_asiento=request.POST['num_asiento'])
        cta = get_object_or_404(cuenta, pk=request.POST['num_cuenta'])
        tipo_mov = request.POST['tipo_movimiento']

        if tipo_mov == "1":
            aux_libro.fecha = request.POST['fecha_emision']
            aux_libro.concepto = request.POST['id_concepto']
            aux_libro.num_cuenta = cta
            aux_libro.debe = request.POST['id_monto']

            aux_libro.save()
            
        elif tipo_mov == "2":             
            aux_libro.fecha = request.POST['fecha_emision']
            aux_libro.concepto = request.POST['id_concepto']
            aux_libro.num_cuenta = cta
            aux_libro.haber = request.POST['id_monto']
            
            aux_libro.save()

        mensaje_error = "Asiento actualizado!!"
        return render(request, 'cargar_asiento_diario.html', {"libros_diarios": libros_diarios, "cuentas": cuentas, "mensaje_error": mensaje_error})
    else:
        mensaje_error = "Asiento no esta cargado."

        return render(request, 'cargar_asiento_diario.html', {"libros_diarios": libros_diarios, "cuentas": cuentas, "mensaje_error": mensaje_error})




#-------------------------------------------------------------------------------------------------------------------------

def create_proveedor(request):
    return render('/gestor/')



def create_client(request):
    return render('/gestor/')



def asistencia_contable(request):
    return render('/gestor/')


