import pysftp
from xml.dom import minidom
import os
from dateutil import parser
import datetime
from .ordenes_compra import *
from .funciones_bodega_internos import *

# Produccion
myHostname = "fierro.ing.puc.cl"
myUsername = "grupo6"
myPassword = "jWTyw7cGzq3enuS48"

'''

# Desarollo
myHostname = "fierro.ing.puc.cl"
myUsername = "grupo6_dev"
myPassword = "hhqC9wWbKyIMjPX"
'''


#cnopts = pysftp.CnOpts()
#cnopts.hostkeys = None

#Copia todos los archivos de los pedidos, desde el servidor a la carpeta pedidos
def copiar_pedidos():

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        #print("Connection succesfully stablished ... ")

        # Switch to a remote directory
        sftp.cwd('/pedidos')

        # Obtain structure of the remote directory '/var/www/vhosts'
        directory_structure = sftp.listdir_attr()

        sftp.get_r('/', './')


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
def obtener_tiempo_restante(orden):
    dt = parser.parse(orden['fechaEntrega']).replace(tzinfo=None)
    hora = datetime.datetime.now() - datetime.timedelta(hours=4)
    return dt-hora



def revisar_posibilidad_entrega2(orden_compra):
    print('revisando posibilidad de entrega a otro grupo')
    orden = orden_compra[0]
    sku = orden['sku']
    cantidad = orden['cantidad']
    tiempo = obtener_tiempo_restante(orden)
    print('logramos obtener el tiempo restante: {}'.format(tiempo))
    # Si tengo productos necesarios y margen de 5 min de despacho
    if tiempo > datetime.timedelta(minutes=5):
        stock = contar_productos()
        if sku in stock.keys():
            print('tengo {} y me piden {}'.format(stock[sku], cantidad))
            if stock[sku] >= cantidad:
                return 0
        else:
            print('el sku pedido no esta en mi inventario')
            return 1
    else:
        print('No hay suficiente tiempo para entregar el producto')
        return 2


# Retorna True si es posibe completar la entrega, False en caso contrario
def revisar_posibilidad_entrega(orden_compra):
    orden = orden_compra[0]
    sku = orden['sku']
    cantidad = orden['cantidad']
    tiempo = obtener_tiempo_restante(orden)
    # Si tengo productos necesarios y margen de 5 min de despacho
    if tiempo > datetime.timedelta(minutes=5):
        stock = contar_productos()
        if sku in stock.keys():
            if stock[sku] >= cantidad:
                print('tengo {} y me piden {}'.format(stock[sku], cantidad))
                return 0

    # Si tengo ventana de 30 para conicar productos
    if tiempo > datetime.timedelta(minutes=10):
        # Tengo para fabricar inmediatamente
        if fabricable_multiplo(sku, cantidad):
            print('puedo fabricar lo que me piden')
            return 1
        # Debo fabricar subproductos
        else:
            print('no puedo fabricar lo que me piden')
            return 2

    # No tendre tiempo para entregar
    print('No hay suficiente tiempo para entregar')
    return 3

# Funcion que elimina archivo en el servidor y local
def borrar_archivo(archivo):
    # Elimina del servidor #, cnopts=cnopts
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        #print("Connection succesfully stablished ... ")
        # Switch to a remote directory
        sftp.cwd('/pedidos')
        for file in archivo:
            try:
                sftp.remove(file)
            except:
                pass

    # Si el archivo existe lo elimina localmente
    for file in archivo:
        try:
            if os.path.isfile(os.getcwd()+'/pedidos/'+file):
                os.remove(os.getcwd()+'/pedidos/'+file)
                print('Correctly remove {}'.format(file))
            #si no, print error
            else:    ## Show an error ##
                print("Error: {} file not found".format(file))
        except:
            pass
