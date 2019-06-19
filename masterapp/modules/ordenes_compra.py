from .constantes import *
import requests
import json
import time


# Retorna la fecha anual en milisegundos
def fecha_actual():
    millis = int(round(time.time() * 1000))
    return millis

# Crea una orden de compra, la orden de compra se recibira en los minutos indicados
# El parametro canal debe ser "b2b"o "b2c"
# Falta agregar la opcion de Url de notificacion
def crear_oc(proveedor, sku, minutos, cantidad, precio, canal):
    url = 'https://integracion-2019-{}.herokuapp.com/oc/crear'.format(ambiente)

    headers = {'content-type': 'application/json'}

    milisegundos = fecha_actual() + int(round(minutos * 60000))

    payload = {'cliente': id_grupos[grupo], 'proveedor': id_grupos[proveedor], 'sku': int(sku), 'fechaEntrega': milisegundos, 'cantidad': int(cantidad), 'precioUnitario': int(precio), 'canal': str(canal)}

    r = requests.put(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        lista = json.loads(r.text)
        print('Orden de compra creada exitosamente')
        print(lista)
        return lista
    else:
        print('Error creando orden de compra')
        return False


def obtener_oc(id):
    url = 'https://integracion-2019-{}.herokuapp.com/oc/obtener/{}'.format(ambiente, id)

    headers = {'content-type': 'application/json'}

    payload = {'id': str(id)}

    r = requests.get(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        lista = json.loads(r.text)
        return lista
    else:
        return False

def aceptar_oc(id):
    url = 'https://integracion-2019-{}.herokuapp.com/oc/recepcionar/{}'.format(ambiente, id)

    headers = {'content-type': 'application/json'}

    payload = {'id': str(id)}

    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        lista = json.loads(r.text)
        return lista
    else:
        return False

def rechazar_oc(id, motivo):
    url = 'https://integracion-2019-{}.herokuapp.com/oc/rechazar/{}'.format(ambiente, id)

    headers = {'content-type': 'application/json'}

    payload = {'id': str(id), 'rechazo': str(motivo)}

    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        lista = json.loads(r.text)
        return lista
    else:
        return False

def anular_oc(id, motivo):
    url = 'https://integracion-2019-{}.herokuapp.com/oc/anular/{}'.format(ambiente, id)

    headers = {'content-type': 'application/json'}

    payload = {'id': str(id), 'anulacion': str(motivo)}

    r = requests.delete(url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        lista = json.loads(r.text)
        return lista
    else:
        return False
