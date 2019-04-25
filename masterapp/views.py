from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .modules.funciones_bodega import *

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
