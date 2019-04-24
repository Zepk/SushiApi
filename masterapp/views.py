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
