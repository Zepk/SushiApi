from .constantes import *
from .hashing import *
import requests
import json

# Consultar por almacenes del grupo
def obtener_almacenes():
    mensaje = "GET"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/almacenes'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization": "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code


def obtener_productos_en_almacen(almacenId, sku):
    mensaje = "GET{}{}".format(almacenId, sku)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/stock?almacenId={}&sku={}'.format(ambiente, almacenId, sku)
    headers = {'content-type': 'application/json', "Authorization": "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


# Consultar por skus con stock en un almacen, pide la id del almacen
def obtener_skus_con_stock(id_almacen):
    mensaje = "GET{}".format(id_almacen)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/skusWithStock?almacenId={}'.format(ambiente, id_almacen)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code


def mover_productos_entre_almacenes(id_producto, id_almacen):
    mensaje = "POST{}{}".format(id_producto, id_almacen)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/moveStock'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization": "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"productoId": id_producto, "almacenId": id_almacen}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        print(r.text)
        return r.status_code


def mover_productos_entre_bodegas(id_producto, id_almacen, id_orden):
    mensaje = "POST{}{}".format(id_producto, id_almacen)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/moveStockBodega'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization": "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"productoId": id_producto, "almacenId": id_almacen, "precio": 10, "oc":  id_orden}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        return r
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r


def fabricar_producto(sku, cantidad):
    mensaje = "PUT{}{}".format(sku, cantidad)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/fabrica/fabricarSinPago'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"sku": sku, "cantidad": int(cantidad)}
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    print(r.text)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


def fabrica_obtener_cuenta():
    mensaje = "GET"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/fabrica/getCuenta'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


def eliminar_hook():
    mensaje = "DELETE"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/hook'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.delete(url, headers=headers)
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


def obtener_hook():
    mensaje = "GET"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/hook'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


def setear_hook(url):
    mensaje = "PUT{}".format(url)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/hook'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"url": url}
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code

# Funcion OK
def obtener_inventario_otro_grupo(grupo):
    url = 'http://tuerca{}.ing.puc.cl/inventories'.format(grupo)
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code


# Todavia no sabemos si esta OK, retorna {sku: hola} por mientras
# Puede que el header este malo
def pedir_orden_producto(sku, cantidad, almacenId, grupo, id_oc):
    url = 'http://tuerca{}.ing.puc.cl/orders/'.format(grupo)
    headers = {'content-type': 'application/json', 'group': '6'}
    payload = {'sku': str(sku), 'cantidad': cantidad, 'almacenId': str(almacenId), 'oc': id_oc}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r


def pedir_orden_producto2(sku, cantidad, almacenId, grupo, id_oc):
    url = 'http://tuerca{}.ing.puc.cl/orders'.format(grupo)
    headers = {'content-type': 'application/json', 'group': '6'}
    payload = {'sku': str(sku), 'cantidad': cantidad, 'almacenId': str(almacenId), 'oc': id_oc}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r

# PAra nuevos pedidos otros pedir_a_grupos
def obtener_inventario_grupo(grupo):
    url = 'http://tuerca{}.ing.puc.cl/inventories'.format(grupo)
    headers = {'content-type': 'application/json', 'group': '6'}
    r = requests.get(url, headers=headers)
    return r

def despachar_producto(id, oc, direccion, precio):
    mensaje = "DELETE{}{}{}{}".format(id, direccion, precio, oc)
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-{}.herokuapp.com/bodega/stock'.format(ambiente)
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {'productoId': str(id), 'oc': str(oc), 'direccion': str(direccion), 'precio': int(precio)}
    r = requests.delete(url, headers=headers, data=json.dumps(payload))
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code
