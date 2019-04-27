from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .modules.funciones_bodega import *
from django.http.response import JsonResponse
import json
# Endpoint necesarios, los que se entregaron todos los grupos


def inventories(request):
    if request.method == "GET":
        almacenes = obtener_almacenes()
        inventario = {}
        for almacen in almacenes.json():
            if int(almacen["usedSpace"]) > 0:
                for skus in obtener_skus_con_stock(almacen["_id"]).json():
                    if skus["_id"] in inventario.keys():
                        inventario[skus["_id"]] += skus["total"]
                    else:
                        inventario[skus["_id"]] = skus["total"]
        respuesta = []
        for k, v in inventario.items():
            respuesta.append({"sku": k, "total": v})
        return JsonResponse(respuesta, status=200, safe=False)
    else:
        return JsonResponse({'status_text': 'method /{}/ not valid'.format(request.method)}, status=405)


# ELIMINAR ESTAS VIEWS, estan solo de apoyo para probar las funciones_bodega
def moveStock(request):
    output = mover_productos_entre_almacenes(request.GET.get('almacenId', None),
                                             request.GET.get('productoId', None))
    template = loader.get_template('masterapp/index.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def moveStockBodega(request):
    output = mover_productos_entre_bodegas(request.GET.get('productoId', None),
                                           request.GET.get('almacenId', None))
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
    output = obtener_productos_en_almacen(request.GET.get('almacenId', None), request.GET.get('sku', None))
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
    output = fabricar_producto(request.GET.get('sku', None), request.GET.get('cantidad', None))
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def getCuenta(request):
    output = fabrica_obtener_cuenta()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def eliminarhook(request):
    output = eliminar_hook()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def obtenerhook(request):
    output = obtener_hook()
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def setearhook(request):
    output = setear_hook(request.GET.get('url', None))
    template = loader.get_template('masterapp/output_view.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))
