from celery import shared_task
import json
from .modules.funciones_bodega import *
from .modules.funciones_bodega_internos import *

# mueve periodicamente los productos de pulmon y recepcion a almacenes de proposito general
# Falta tomar en cuenta que no todos los productos son de tamano 1
@shared_task
def vaciar_recepcion_y_pulmon():
    almacenes = json.loads(obtener_almacenes())
    for almacen in almacenes:
        if (almacen['_id'] == pulmon or almacen['_id'] == recepcion) and almacen['usedSpace'] != 0:
            for almacen2 in almacenes:
                if almacen2['_id'] == almacen_general1 or almacen2['_id'] == almacen_general2:
                    if almacen2['totalSpace'] > almacen2['usedSpace']:
                        skus = json.loads(obtener_skus_con_stock(almacen['_id']))
                        for sku in skus:
                            sku = sku['_id']
                            productos = json.loads(obtener_productos_en_almacen(almacen['_id'], sku))
                            for producto in productos:
                                mover_productos_entre_almacenes(producto['_id'], almacen2['_id'])

# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_propios():
    diccionario = contar_productos()

    for sku in skus_propios:
        if sku not in diccionario.keys():
            fabricar_producto(sku, unidades_por_lote[sku])
        elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku]:
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            print('pidiendo productos')



