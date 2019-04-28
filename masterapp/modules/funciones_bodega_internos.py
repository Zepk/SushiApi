from .constantes import *
from .hashing import *
import requests
import json
from .funciones_bodega import *


def stock_disponible():
    almacenes = obtener_almacenes()
    inventario = {}
    for almacen in json.loads(almacenes):
        if int(almacen["usedSpace"]) > 0:
            for skus in json.loads(obtener_skus_con_stock(almacen["_id"])):
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


def obtener_almacenes_con_sku(sku):
    almacenes = obtener_almacenes()
    inventario = {}
    for almacen in json.loads(almacenes):
        if int(almacen["usedSpace"]) > 0:
            for skus in json.loads(obtener_skus_con_stock(almacen["_id"])):
                if skus["_id"] == sku:
                    inventario[almacen["_id"]] = {"sku": skus["_id"], "total": skus["total"], "despacho": almacen["despacho"]}
                    break
    return inventario


def despachar_pedido_bodega(sku, cantidad, almacenId):
    almacen_despachoId = "5cbd3ce444f67600049431d2"
    almacenes = obtener_almacenes_con_sku(sku)
    despachados = 0
    for almacen in almacenes.keys():
        productos = json.loads(obtener_productos_en_almacen(almacen, sku))
        print(productos)
        for producto in productos:
            if almacenes[almacen]["despacho"]:
                if despachar_un_producto(producto["_id"], almacenId, 10):
                    print('OK {}\n'.format(almacen))
                    despachados += 1
            else:
                mover_productos_entre_almacenes(almacen_despachoId, producto["_id"])
                if despachar_un_producto(producto["_id"], almacenId, 10):
                    print('OK {}\n'.format(almacen))
                    despachados += 1
            if despachados == cantidad:
                print(cantidad , despachados)
                return True
    return False


def despachar_un_producto(productoId, almacenId, precio):
    r = mover_productos_entre_bodegas(productoId, almacenId)
    if r.status_code == 200:
        return True
    else:
        return False
