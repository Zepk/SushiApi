from celery import shared_task
import json
from .modules.funciones_bodega import *
from .modules.funciones_bodega_internos import *
import random
from time import sleep
from .modules.sftp import *

# mueve periodicamente los productos de pulmon y recepcion a almacenes de proposito general
# Falta tomar en cuenta que no todos los productos son de tamano 1
@shared_task
def vaciar_recepcion_y_pulmon():
    try:
        almacenes = json.loads(obtener_almacenes())
        for almacen in almacenes:
            if (almacen['_id'] == pulmon or almacen['_id'] == recepcion) and almacen['usedSpace'] != 0:
                for almacen2 in almacenes:
                    if almacen2['_id'] == almacen_general1 or almacen2['_id'] == almacen_general2:
                        if int(almacen2['totalSpace']) > int(almacen2['usedSpace']) + 30:
                            skus = json.loads(obtener_skus_con_stock(almacen['_id']))
                            for sku in skus:
                                sku = sku['_id']
                                productos = json.loads(obtener_productos_en_almacen(almacen['_id'], sku))
                                for producto in productos:
                                    if int(almacen2['totalSpace']) > int(almacen2['usedSpace']) + 30:
                                        mover_productos_entre_almacenes(producto['_id'], almacen2['_id'])
                                    else:
                                        break
    except TypeError:
        pass
@shared_task
def vaciar_pulmon():
    try:
        almacenes = json.loads(obtener_almacenes())
        for almacen in almacenes:
            if almacen['_id'] == pulmon and almacen['usedSpace'] != 0:
                skus = json.loads(obtener_skus_con_stock(almacen['_id']))
                for sku in skus:
                    sku = sku['_id']
                    productos = json.loads(obtener_productos_en_almacen(almacen['_id'], sku))
                    for producto in productos:
                        if obtener_espacio_almacen(almacen_general1) > 20:
                            mover_productos_entre_almacenes(producto['_id'], almacen_general1)
                        elif obtener_espacio_almacen(almacen_general2) > 20:
                            mover_productos_entre_almacenes(producto['_id'], almacen_general2)
                        else:
                            return False
    except TypeError:
        pass






# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes o 300 unidades
@shared_task
def pedir_productos_propios():
    diccionario = contar_productos()
    for sku in skus_propios:
        if sku == '1003' or sku == '1007':
            continue
        if sku not in diccionario.keys():
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            #print('pidiendo productos {}'.format(sku))
        #elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku] and
        elif diccionario[sku] < stock_minimal[sku]:
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            #print('pidiendo productos {}'.format(sku))

@shared_task
def pedir_azucar():
    print('revisando si es necesario pedir azucar')
    diccionario = contar_productos()
    sku = '1003'
    if sku not in diccionario.keys():
        fabricar_producto(sku, str(unidades_por_lote[sku]))
        #print('pidiendo productos {}'.format(sku))
    #elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku] and
    elif diccionario[sku] < stock_minimal[sku]:
        fabricar_producto(sku, str(unidades_por_lote[sku]))
        #print('pidiendo productos {}'.format(sku))

@shared_task
def pedir_salmon():
    diccionario = contar_productos()
    sku = '1003'
    if sku not in diccionario.keys():
        fabricar_producto(sku, str(unidades_por_lote[sku]))
        #print('pidiendo productos {}'.format(sku))
    #elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku] and
    elif diccionario[sku] < stock_minimal[sku]:
        fabricar_producto(sku, str(unidades_por_lote[sku]))
        #print('pidiendo productos {}'.format(sku))




# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_ajenos():
    diccionario = contar_productos()
    for sku, grupos in produccion_otros.items():
        # print('El sku {}'.format(sku))
        if sku not in diccionario.keys():
            # print('SKU no se tenia')
            for g in grupos:
                print('1 Se pide {} al grupo {}'.format(sku, g))
                inventario = False
                try:
                    r = obtener_inventario_grupo(g)
                    if r.status_code == 200:
                        inventario = json.loads(r.text)
                        #print(inventario)
                    else:
                        # print('No da inventario')
                        pass
                except:
                    pass
                if inventario:
                    try:
                        for producto in inventario:
                            if sku == producto['sku'] and producto['total'] >= 3:
                                #print(inventario)
                                #print('Tienen inventario ')
                                oc = crear_oc(int(g), sku, 80, 3, 1, 'b2b')
                                # print(oc['_id'])
                                r1 = pedir_orden_producto2(sku, 3, recepcion, g, oc['_id'])
                                r2 = pedir_orden_producto(sku, 3, recepcion, g, oc['_id'])
                                if r1.status_code == 200 or r1.status_code == 201:
                                    #print(r1.text)
                                    #print('Request exitosa 1')
                                    break
                                if r2.status_code == 200 or r2.status_code == 201:
                                    #print(r1.text)
                                    #print('Request exitosa 2')
                                    break
                                #print('Anular request {}  {}'.format(r1, r2))
                                r_oc = anular_oc(oc['_id'], 'Grupo no responde a request  con 200 o 201')
                                # print(r_oc)
                    except:
                        pass
        #elif diccionario[sku] < lotes_minimos_materia_prima_ajena * unidades_por_lote[sku]:
        elif diccionario[sku] < stock_minimal[sku]:
            # print('SKU bajo stock minimo')
            for g in grupos:
                #print(' 2 Se pide {} al grupo {}'.format(sku, g))
                inventario = False
                try:
                    r = obtener_inventario_grupo(g)
                    if r.status_code == 200:
                        inventario = json.loads(r.text)
                        #print(inventario)
                    else:
                        # print('No da inventario')
                        pass
                except:
                    pass
                if inventario:
                    try:
                        for producto in inventario:
                            if sku == producto['sku'] and producto['total'] >= 3:
                                #print(inventario)
                                #print('Tienen inventario ')
                                oc = crear_oc(int(g), sku, 80, 3, 1, 'b2b')
                                # print(oc['_id'])
                                r1 = pedir_orden_producto2(sku, 3, recepcion, g, oc['_id'])
                                r2 = pedir_orden_producto(sku, 3, recepcion, g, oc['_id'])
                                if r1.status_code == 200 or r1.status_code == 201:
                                    #print(r1.text)
                                    #print('Request exitosa 1')
                                    break
                                if r2.status_code == 200 or r2.status_code == 201:
                                    #print(r1.text)
                                    #print('Request exitosa 2')
                                    break
                                #print('Anular request {}  {}'.format(r1, r2))
                                r_oc = anular_oc(oc['_id'], 'Grupo no responde a request  con 200 o 201')
                                # print(r_oc)
                    except:
                        pass
        # print('\n')


# La funcion se encarga de producir los productos que podemos producir con las materias primas que podemos producir
# Cambio de propopsito, hace todo lo de la fabrica
@shared_task
def fabricar_productos_propios():
    stock = contar_productos()
    for sku in stock_minimo.keys():
        # Si ya tenemos del producto, revisamos si tenemos menos que lo que queremos, en ese caso poducimos, si no, noo
        if sku == '1013':
            continue
        elif sku in stock.keys():
            #print(sku, stock[sku], delta_stock_minimo * stock_minimo[sku])
            #if stock[sku] < delta_stock_minimo * stock_minimo[sku] or
            if stock[sku] < stock_minimal[sku]:
                if fabricable(sku, stock):
                    preparar_despacho(recetas[sku])
                    #print("Fabricando {}".format(nombres[sku]))
                    fabricar_producto(sku, unidades_por_lote[sku])
                else:
                    continue
        # Si no tenemos del producto, lo producimos
        else:
            #print(sku)
            if fabricable(sku, stock):
                preparar_despacho(recetas[sku])
                #print("Fabricando {}".format(nombres[sku]))
                fabricar_producto(sku, unidades_por_lote[sku])
            else:
                continue

@shared_task
def despachar_pedido_bodega_smarter(sku, cantidad, almacenId, id_orden):
    despachados = 0
    while True:
        #sleep(1)
        producto = elegir_producto_a_despachar(sku)
        if not producto[0]:
            #print("no hay producto")
            continue
        if not producto[1]:
            #print('moviendo producto entre almacenes')
            mover_productos_entre_almacenes(producto[0]["_id"], despacho)
            if despachar_un_producto(producto[0]["_id"], almacenId, 10, id_orden):
                despachados += 1
            if despachados >= cantidad:
                aceptar_oc(id_orden)
                print('Orden B2B Completada exitosamente')
                return True
        else:
            #print("intentando despachar")
            if despachar_un_producto(producto[0]["_id"], almacenId, 10, id_orden):
                despachados += 1
            if despachados >= cantidad:
                aceptar_oc(id_orden)
                print('Orden B2B Completada exitosamente')
                return True
    return False


def elegir_producto_a_despachar(sku):
    #primer elemento de la respuesta es el producto, el segundo es un boleand que es true si el producto esta en despahco, y false en caso contrario
    almacenes = obtener_almacenes_con_sku(sku)
    try:
        productos = json.loads(obtener_productos_en_almacen(despacho, sku))
        producto = random.choice(productos)
        respuesta = (producto, True)
        #print('elegimos un producto para despachar')
        return respuesta
    except TypeError:
        pass
    except IndexError:
        pass

    for almacen in almacenes.keys():
        if not almacenes[almacen]["despacho"]:
            try:
                productos = json.loads(obtener_productos_en_almacen(almacen, sku))
            except TypeError:
                continue
            producto = random.choice(productos)
            respuesta = (producto, False)
            #rint('elegimoos un producto para despachar')
            return respuesta
    return (False, False)



@shared_task
def vaciar_despacho():
    try:
        almacenes = json.loads(obtener_almacenes())
        for almacen in almacenes:
            if (almacen['_id'] == despacho) and almacen['usedSpace'] != 0:
                for almacen2 in almacenes:
                    if almacen2['_id'] == almacen_general1 or almacen2['_id'] == almacen_general2:
                        if almacen2['totalSpace'] > almacen2['usedSpace'] + 3:
                            skus = json.loads(obtener_skus_con_stock(almacen['_id']))
                            for sku in skus:
                                sku = sku['_id']
                                productos = json.loads(obtener_productos_en_almacen(almacen['_id'], sku))
                                for producto in productos:
                                    if almacen2['totalSpace'] > almacen2['usedSpace']:
                                        mover_productos_entre_almacenes(producto['_id'], almacen2['_id'])
                                    else:
                                        break
    except TypeError:
        pass

@shared_task
def fabricar_productos_intermedios():
    stock = contar_productos()
    for sku in stock_deseado_productos_intermedios.keys():
        # Si ya tenemos del producto, revisamos si tenemos menos que lo que queremos, en ese caso poducimos, si no, noo
        if sku == '1013':
            continue
        elif sku in stock.keys():
            #if stock[sku] < delta_stock_minimo * stock_deseado_productos_intermedios[sku] or
            if stock[sku] < stock_minimal[sku]:
                if fabricable(sku, stock):
                    preparar_despacho(recetas[sku])
                    #print("Fabricando {}".format(nombres[sku]))
                    fabricar_producto(sku, unidades_por_lote[sku])
                else:
                    continue
        # Si no tenemos del producto, lo producimos
        else:
            #print(sku)
            if fabricable(sku, stock):
                preparar_despacho(recetas[sku])
                #print("Fabricando {}".format(nombres[sku]))
                fabricar_producto(sku, unidades_por_lote[sku])
            else:
                continue


@shared_task
def cocinar(sku, cantidad):
    preparar_cocina(recetas[sku], cantidad)
    fabricar_producto(sku, cantidad)

@shared_task
def despachar_a_cliente(sku, cantidad, direccion, precio, oc):
    preparar_despacho_cliente(sku, cantidad)
    productos = json.loads(obtener_productos_en_almacen(despacho, sku))
    counter = 0
    for producto in productos:
        if producto['sku'] == sku:
            if despachar_producto(producto['_id'], oc, direccion, precio):
                counter += 1
                print('he despachado {} de {}'.format(oc, oc))
                if counter == cantidad:
                    break


@shared_task
def manejar_pedidos_cliente():
    # Copia lo del servidor ftp a local
    copiar_pedidos()
    # Reviso los pedidos en localmente
    pedidos = leer_pedidos_ftp()
    archivos_a_borrar = []
    for pedido in pedidos:
        orden_compra = obtener_oc(pedido['id'])
        if orden_compra:
            posibilidad = revisar_posibilidad_entrega(orden_compra)
            delta = orden_compra[0]['cantidad'] - orden_compra[0]['cantidadDespachada']
            # Rechazo
            if posibilidad == 3:
                rechazar_oc(pedido['id'], 'Poco tiempo')
                archivos_a_borrar.append(pedido['archivo'])
            # Faltan ingredientes intermedios
            elif posibilidad == 2:
                pass
            # Busco cocinar
            elif posibilidad == 1:
                cocinar(pedido['sku'], delta)
            elif posibilidad == 0:
                despachar_a_cliente(pedido['sku'], delta, 'b2c', 1000, pedido['id'])
                orden_compra = obtener_oc(pedido['id'])
                delta_final = orden_compra[0]['cantidad'] - orden_compra[0]['cantidadDespachada']
                if delta_final <= 0:
                    aceptar_oc(pedido['id'])
                    print('********')
                    print('Orden FTP Completada exitosamente')
                    print('********')
                    archivos_a_borrar.append(pedido['archivo'])
    borrar_archivo(archivos_a_borrar)
