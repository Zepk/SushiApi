from celery import shared_task
import json
from .modules.funciones_bodega import *

@shared_task
def vaciar_recepcion_y_pulmon():
    almacenes = json.loads(obtener_almacenes())
    for almacen in almacenes:
        if almacen['_id'] == pulmon and almacen['usedSpace'] != 0:
            for almacen2  in almacenes:
                if almacen2['_id'] == almacen_general1 or almacen2['_id'] == almacen_general2:
                    if almacen2['totalSpace'] > almacen2['usedSpace']:
                        skus = json.loads(obtener_skus_con_stock(pulmon))
                        for sku in skus:
                            sku = sku['_id']
                            productos = json.loads(obtener_productos_en_almacen(pulmon, sku))
                            for producto in productos:
                                mover_productos_entre_almacenes(producto['_id'], almacen2['_id'])


@shared_task
def probando_celery():
    print('Probando Celery \n')
