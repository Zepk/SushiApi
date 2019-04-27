from .constantes import *
from .hashing import *
import requests
import json
from .funciones_bodega import *


def stock_disponible():
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
    return respuesta


def stock_disponible_sku(sku, cantidad):
    respuesta = stock_disponible()
    for r in respuesta:
        if sku == r["sku"] and r["total"] >= cantidad:
            return True
    return False


def despachar_pedido(sku, cantidad, almacenId):
    pass
