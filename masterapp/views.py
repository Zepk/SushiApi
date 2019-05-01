from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .modules.funciones_bodega import *
from .modules.funciones_bodega_internos import *
from .tasks import *
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
            despachar_pedido_bodega.delay(sku, cantidad, almacenId)
            aceptado = True
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
# Create your views here.


def index(request):
    almacenes = obtener_almacenes()
    template = loader.get_template('masterapp/index.html')
    context = {
        'almacenes': almacenes,
    }
    return HttpResponse(template.render(context, request))


def productos_en_almacen(request):
    productos = obtener_productos_en_almacen(request.GET.get('almacenId', None), request.GET.get('sku', None))
    template = loader.get_template('masterapp/productos_en_almacen.html')
    context = {
        'productos': productos,
    }
    return HttpResponse(template.render(context, request))


def skus_stock(request):
    skus = obtener_skus_con_stock(request.GET.get('almacenId', None))
    template = loader.get_template('masterapp/sku_stock.html')
    context = {
        'skus': skus,
    }
    return HttpResponse(template.render(context, request))


def fabricar_sin_pagar(request):
    producto = fabricar_producto(request.GET.get('sku', None), request.GET.get('cantidad', None))
    template = loader.get_template('masterapp/fabricar_sin_pagar.html')
    context = {
        'producto': producto,
    }
    return HttpResponse(template.render(context, request))


def obtener_cuenta(request):
    cuenta = fabrica_obtener_cuenta()
    template = loader.get_template('masterapp/obtener_cuenta.html')
    context = {
        'cuenta': cuenta,
    }
    return HttpResponse(template.render(context, request))


def obtener_eliminar_hook(request):
    hook = eliminar_hook()
    template = loader.get_template('masterapp/hook.html')
    context = {
        'hook': hook,
    }
    return HttpResponse(template.render(context, request))


def obtener_obtener_hook(request):
    hook = obtener_hook()
    template = loader.get_template('masterapp/hook.html')
    context = {
        'hook': hook,
    }
    return HttpResponse(template.render(context, request))


def obtener_setear_hook(request):
    hook = setear_hook(request.GET.get('url', None))
    template = loader.get_template('masterapp/hook.html')
    context = {
        'hook': hook,
    }
    return HttpResponse(template.render(context, request))
