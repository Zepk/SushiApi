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
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code
