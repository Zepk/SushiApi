from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .modules.funciones_bodega import *
from .modules.funciones_bodega_internos import *
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


grupo = 6


# ENDPOINTS NECESARIOS, los que se entregaron todos los grupos
# DAr lista de productos que teneos
def inventories(request):
    if request.method == "GET":
        respuesta = stock_disponible()
        return JsonResponse(respuesta, status=200, safe=False)
    else:
        return JsonResponse({'status_text': 'method /{}/ not valid'.format(request.method)}, status=405)


# Recibir ordenes de otro grupo
@csrf_exempt
def orders(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            sku = body["sku"]
            cantidad = body["cantidad"]
            almacenId = body["almacenId"]
        except:
            JsonResponse({'status_text': 'Parametros incorrectos'.format(request.method)}, status=400)
        if stock_disponible_sku(sku, cantidad):
            # Falta esta funcion
            aceptado = despachar_pedido_bodega(sku, cantidad, almacenId)
            if aceptado:
                respuesta = {}
                respuesta["sku"] = sku
                respuesta["cantidad"] = True
                respuesta["almacenId"] = almacenId
                respuesta["grupo"] = grupo
                respuesta["aceptado"] = aceptado
                respuesta["despachado"] = aceptado
                return JsonResponse(respuesta, status=200)
            else:
                return JsonResponse({'status_text': 'No pudimos despachar el pedido'.format(request.method)}, status=400)
        else:
            return JsonResponse({'status_text': 'No tenemos Stock'.format(request.method)}, status=404)
    else:
        return JsonResponse({'status_text': 'method /{}/ not valid'.format(request.method)}, status=405)


# ELIMINAR ESTAS VIEWS, estan solo de apoyo para probar las funciones_bodega
def moveStock(request):
    output = mover_productos_entre_almacenes(request.GET.get('almacenId', None),
                                             request.GET.get('productoId', None)).json()
    template = loader.get_template('masterapp/index.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def moveStockBodega(request):
    output = mover_productos_entre_bodegas(request.GET.get('productoId', None),
                                           request.GET.get('almacenId', None)).json()
    template = loader.get_template('masterapp/index.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def almacenes(request):
    almacenes = obtener_almacenes().json()
    template = loader.get_template('masterapp/index.html')
    context = {
        'almacenes': almacenes,
    }
    return HttpResponse(template.render(context, request))


def stockAlmacen(request):
    output = obtener_productos_en_almacen(request.GET.get('almacenId', None), request.GET.get('sku', None)).json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def skusWithStock(request):
    output = obtener_skus_con_stock(request.GET.get('almacenId', None)).json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def fabricarSinPago(request):
    output = fabricar_producto(request.GET.get('sku', None), request.GET.get('cantidad', None)).json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def getCuenta(request):
    output = fabrica_obtener_cuenta().json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def eliminarhook(request):
    output = eliminar_hook().json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def obtenerhook(request):
    output = obtener_hook().json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def setearhook(request):
    output = setear_hook(request.GET.get('url', None)).json()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))
