
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,  redirect
from gestor.apps.contable.libro_diario.models import cuenta, libro_diario, detalle_libro_diario
from gestor.apps.producto.models import (producto)
from gestor.apps.inventario.models import (inventario)
from gestor.apps.contable.libro_mayor.models import (libro_mayor)
from django.views.decorators.cache import never_cache


def get_chart(request):
    produc = producto.objects.all()

    chart = {
        'tooltip': {
            'show': True,
            'trigger': "axis",
            'triggerOn': "mousemove|click"
        },
        'xAxis': [
            {
                'type': "category",
                'data': []
            }
        ],
        'yAxis': [
            {
                'type': "value"
            }
        ],
        'series': []
    }

    colors = ['blue', 'orange', 'red', 'black', 'yellow',
              'green', 'magenta', 'lightblue', 'purple', 'brown']

    for idx, p in enumerate(produc):
        fecha_labels = []
        fecha_labels_aux = []
        stock_accumulative = []
        current_stock = 0

        linea = inventario.objects.filter(cod_producto=p).order_by('fecha')
        for l in linea:
            fecha_labels.append(l.fecha.strftime('%Y-%m-%d'))
            fecha_labels_aux.append(l.fecha.strftime('%Y-%m-%d'))
            if l.tipo_movimiento:
                current_stock += l.cantidad
            else:
                current_stock -= l.cantidad
            stock_accumulative.append(current_stock)

        random_color = colors[idx % len(colors)]

        chart['series'].append({
            'name': p.descripcion,
            'data': stock_accumulative,
            'type': "line",
            'itemStyle': {'color': random_color},
        })

        # Asegúrate de que todas las series tengan la misma fecha_labels (eje X)
        chart['xAxis'][0]['data'] = fecha_labels_aux

    return JsonResponse(chart)


@never_cache
def get_chart2(request):
    produc = cuenta.objects.all()

    chart1 = {
        'tooltip': {
            'show': True,
            'trigger': "axis",
            'triggerOn': "mousemove|click"
        },
        'xAxis': [
            {
                'type': "category",
                'data': []
            }
        ],
        'yAxis': [
            {
                'type': "value"
            }
        ],
        'series': []
    }

    colors = ['blue', 'orange', 'red', 'black', 'yellow',
              'green', 'magenta', 'lightblue', 'purple', 'brown']

    for idx, p in enumerate(produc):
        fecha_labels = []
        fecha_labels_aux = []
        stock_accumulative = []
        current_stock = 0

        linea = libro_mayor.objects.filter(num_cuenta=p).order_by('fecha')
        for l in linea:
            fecha_labels.append(l.fecha.strftime('%Y-%m-%d'))
            fecha_labels_aux.append(l.fecha.strftime('%Y-%m-%d'))
            current_stock += l.debe
            current_stock += l.haber
            stock_accumulative.append(current_stock)

        random_color = colors[idx % len(colors)]

        chart1['series'].append({
            'name': p.descripcion,
            'data': stock_accumulative,
            'type': 'bar',
            'seriesLayoutBy': 'row',
            'emphasis': {
                'focus': 'series'
            },
            'itemStyle': {'color': random_color},
        })

        # Asegúrate de que todas las series tengan la misma fecha_labels (eje X)
        chart1['xAxis'][0]['data'] = fecha_labels_aux

    return JsonResponse(chart1)
 
