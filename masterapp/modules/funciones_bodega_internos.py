from .constantes import *
from .hashing import *
import requests
import json
from .funciones_bodega import *
from .ordenes_compra import obtener_oc

def stock_disponible():
    almacenes = obtener_almacenes()
    inventario = {}
    try:
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
    except TypeError:
        pass

# Retorna un diccionario que contiene todas las claves sku: cantidad_disponible
def contar_productos():
    diccionario = {}
    try:
        for producto in stock_disponible():
            diccionario.update({producto['sku']: producto['total']})
        return diccionario
    except TypeError:
        pass

def stock_disponible_sku(sku, cantidad):
    respuesta = stock_disponible()
    for r in respuesta:
        if sku == r["sku"] and lotes_minimos_despacho * unidades_por_lote[sku] <= int(r["total"]) - int(cantidad) and int(cantidad) <= 2 * int(unidades_por_lote[sku]):
            return True
    return False

def stock_disponible_venta():
    respuesta = stock_disponible()
    disponible = []
    for r in respuesta:
        if r["sku"] in skus_propios:
            if r["total"] - lotes_minimos_despacho * unidades_por_lote[r["sku"]] > 0:
                cantidad_venta = r["total"] - lotes_minimos_despacho * unidades_por_lote[r["sku"]]
                if cantidad_venta <=  2 * int(unidades_por_lote[r["sku"]]):
                    disponible.append({"sku": r["sku"], "total": cantidad_venta})
                else:
                    disponible.append({"sku": r["sku"], "total": 2 * int(unidades_por_lote[r["sku"]])})
    return disponible


def obtener_almacenes_con_sku(sku):
    almacenes = obtener_almacenes()
    inventario = {}
    try:
        for almacen in json.loads(almacenes):
            if int(almacen["usedSpace"]) > 0:
                for skus in json.loads(obtener_skus_con_stock(almacen["_id"])):
                    if skus["_id"] == sku:
                        inventario[almacen["_id"]] = {"sku": skus["_id"], "total": skus["total"], "despacho": almacen["despacho"]}
                        break
        return inventario
    except TypeError:
        pass

def despachar_un_producto(productoId, almacenId, precio, id_orden):
    r = mover_productos_entre_bodegas(productoId, almacenId, id_orden)
    if r.status_code == 200:
        print("Producto enviado")
        print(productoId)
        print('Para otro grupo he despachado {} de un total de {}'.format(obtener_oc(id_orden)[0]['cantidadDespachada'], obtener_oc(id_orden)[0]['cantidad']))
        return True
    else:
        print("fallo el despacho")
        print(r.text)
        print(r.status_code)
        return False


# Dado un diccionario creado con contar_productos(), y un sku, revisa si es posible fabricar 1 lote del sku dado
def fabricable(sku, stock):
    receta = recetas[sku]
    for clave in receta.keys():
        if clave in stock.keys():
            if int(stock[clave]) >= int(receta[clave]):
                continue

            else:
                return False
        else:
            return False
    return True


def fabricable_multiplo(sku, multiplo):
    stock = contar_productos()
    receta = recetas[sku]
    for clave in receta.keys():
        if clave in stock.keys():
            if int(stock[clave]) >= int(receta[clave]) * multiplo:
                continue

            else:
                return False
        else:
            return False
    return True



# Dada una receta, mueve los ingredientes necesarios al almacen de despacho
# Puede faltar que retorne algo cuando este listo
def preparar_despacho(receta):
    for clave in receta.keys():
        sku_ready = False
        for almacen in almacenes_nuestro:
            if almacen != despacho:
                for producto in json.loads(obtener_productos_en_almacen(almacen, clave)):
                    if len(json.loads(obtener_productos_en_almacen(despacho, clave))) < receta[clave]:
                        mover_productos_entre_almacenes(producto['_id'], despacho)

                    else:
                        sku_ready = True
                        break
            if sku_ready:
                break

# Dada una receta, mueve los ingredientes necesarios al almacen de cocina
# Puede faltar que retorne algo cuando este listo
def preparar_cocina(receta, cantidad):
    for clave in receta.keys():
        sku_ready = False
        for almacen in almacenes_nuestro:
            if almacen != cocina:
                for producto in json.loads(obtener_productos_en_almacen(almacen, clave)):
                    if len(json.loads(obtener_productos_en_almacen(cocina, clave))) < receta[clave] * cantidad:
                        mover_productos_entre_almacenes(producto['_id'], cocina)

                    else:
                        sku_ready = True
                        break
            if sku_ready:
                break

def preparar_despacho_cliente(sku, cantidad):
    sku_ready = False
    for almacen in almacenes_nuestro:
        if almacen != despacho:
            for producto in json.loads(obtener_productos_en_almacen(almacen, sku)):
                if len(json.loads(obtener_productos_en_almacen(despacho, sku))) < cantidad:
                    mover_productos_entre_almacenes(producto['_id'], despacho)
                else:
                    sku_ready = True
                    break

        if sku_ready:
            break

def obtener_espacio_almacen(id):
    almacenes = json.loads(obtener_almacenes())
    for almacen in almacenes:
        if almacen['_id'] == id:
            return almacen['totalSpace'] - almacen['usedSpace']
