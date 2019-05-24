import pysftp
from xml.dom import minidom
import os
from dateutil import parser
import datetime
from .ordenes_compra import *
from .funciones_bodega_internos import *

myHostname = "fierro.ing.puc.cl"
myUsername = "grupo6_dev"
myPassword = "hhqC9wWbKyIMjPX"



#Copia todos los archivos de los pedidos, desde el servidor a la carpeta pedidos
def copiar_pedidos():

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... ")

        # Switch to a remote directory
        sftp.cwd('/pedidos')

        # Obtain structure of the remote directory '/var/www/vhosts'
        directory_structure = sftp.listdir_attr()

        sftp.get_r('/pedidos', './', preserve_mtime=True)


# Retorna una lista que contiene diccionarios, donde cada diccionario corresponde a una orden de compra ftp,
# El diccionario contiene la id, sku, y cantidad de la orden
def leer_pedidos_ftp():
    ordenes = []

    for root, dirs, files in os.walk("./pedidos"):

        for filename in files:
            doc = minidom.parse('./pedidos/{}'.format(filename))
            id = doc.getElementsByTagName("id")[0].firstChild.data
            sku = doc.getElementsByTagName("sku")[0].firstChild.data
            qty = doc.getElementsByTagName("qty")[0].firstChild.data

            orden = {'id': id, 'sku': sku, 'qty': qty, 'archivo': filename}

            ordenes.append(orden)

    return ordenes


# retorna cuanto tiempo falta para el deadline de una entrega
def obtener_tiempo_restante(id):
    orden = obtener_oc(id)
    dt = parser.parse(orden[0]['fechaEntrega']).replace(tzinfo=None)
    hora = datetime.datetime.now() - datetime.timedelta(hours=4)
    return dt-hora


# Retorna True si es posibe completar la entrega, False en caso contrario
def revisar_posibilidad_entrega(id):
    orden = obtener_oc(id)[0]
    sku = orden['sku']
    cantidad = orden['cantidad']
    tiempo = obtener_tiempo_restante(id)
    # Si tengo productos necesarios y margen de 10 min de despacho
    if tiempo > datetime.timedelta(minutes=10):
        stock = contar_productos()
        if sku in stock.keys():
            if stock[sku] >= cantidad:
                return 0

    # Si tengo ventana de 1:30 para conicar productos
    if tiempo > datetime.timedelta(hours=1, minutes=30):
        return 1

    # No tendre tiempo para entregar
    return 2

# Funcion que elimina archivo en el servidor y local
def borrar_archivo(archivo):
    # Elimina del servidor
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... ")
        # Switch to a remote directory
        sftp.cwd('/pedidos')
        sftp.remove(archivo)

    # Si el archivo existe lo elimina localmente
    if os.path.isfile(os.getcwd()+'\\pedidos\\'+archivo):
        os.remove(os.getcwd()+'\\pedidos\\'+archivo)
    #si no, print error
    else:    ## Show an error ##
        print("Error: {} file not found".format(archivo))
