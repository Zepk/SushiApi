from .constantes import *
from .hashing import *
import requests


# Consultar por almacenes del grupo
def obtener_almacenes():
    mensaje = "GET"
    aut = security_hash(mensaje, key)
    url = 'https://integracion-2019-dev.herokuapp.com/bodega/almacenes'
    headers = {'content-type': 'application/json', "Authorization" : "INTEGRACION grupo{}:{}".format(grupo, aut)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return r.status_code
