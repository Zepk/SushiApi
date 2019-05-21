import pysftp
from xml.dom import minidom
import os

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

            orden = {'id': id, 'sku': sku, 'qty': qty}

            ordenes.append(orden)

    return ordenes
