from .constantes import *
from .hashing import *
import requests
import json

# Consultar por almacenes del grupo
def obtener_almacenes():
    mensaje = "GET"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/almacenes'
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code


def obtener_productos_en_almacen(almacenId, sku):
    mensaje = "GET"+almacenId+sku
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/stock?almacenId={}&sku={}'.format(almacenId, sku)
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
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/skusWithStock?almacenId={}'.format(id_almacen)
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
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/moveStock'
    headers = {'content-type': 'application/json', "Authorization": "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"productoId": id_producto, "almacenId": id_almacen}
    r = requests.post(url, headers=headers, data=payload)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        print(r.text)
        return r.status_code


def fabricar_producto(sku, cantidad):
    mensaje = "PUT"+sku+cantidad
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/fabrica/fabricarSinPago'
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
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/fabrica/getCuenta'
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
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/hook'
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
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/hook'
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code


def setear_hook(url):
    mensaje = "PUT"+url
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/hook'
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    payload = {"url": url}
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code
