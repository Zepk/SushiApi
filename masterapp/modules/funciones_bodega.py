from .constantes import *
from .hashing import *
import requests
import json

# Consultar por almacenes del grupo
def obtener_almacenes():
    mensaje = "GET5cbd3ce444f67600049431d4"
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
    print(r.text)
    print(r.status_code)
    if r.status_code == 200:
        return r.text
        #si queremos retornar la lista de diccionarios
        #lista = json.loads(r.text)
        #return lista
    else:
        return r.status_code
