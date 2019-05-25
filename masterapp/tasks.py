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
            if (almacen['_id'] == pulmon or almacen['_id'] == recepcion ) and almacen['usedSpace'] != 0:
                for almacen2 in almacenes:
                    if almacen2['_id'] == almacen_general1 or almacen2['_id'] == almacen_general2:
                        if int(almacen2['totalSpace']) > int(almacen2['usedSpace']) + 3:
                            skus = json.loads(obtener_skus_con_stock(almacen['_id']))
                            for sku in skus:
                                sku = sku['_id']
                                productos = json.loads(obtener_productos_en_almacen(almacen['_id'], sku))
                                for producto in productos:
                                    if int(almacen2['totalSpace']) > int(almacen2['usedSpace']) + 3:
                                        mover_productos_entre_almacenes(producto['_id'], almacen2['_id'])
                                    else:
                                        break
    except TypeError:
        pass



# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_propios():
    diccionario = contar_productos()
    for sku in skus_propios:
        if sku not in diccionario.keys():
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            print('pidiendo productos')
        elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku]:
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            print('pidiendo productos')


# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_ajenos():
    diccionario = contar_productos()
    for sku, grupos in produccion_otros.items():
        print('El sku {}'.format(sku))

        if sku not in diccionario.keys():
            for g in grupos:
                print('El grupo {}'.format(g))
                try:
                    pedir_orden_producto(sku, '3', recepcion, g)
                except:
                    pass
                try:
                    pedir_orden_producto2(sku, '3', recepcion, g)
                except:
                    pass
        elif sku == '1013' and diccionario[sku] < delta_stock_minimo * stock_minimo[sku]:
            for g in grupos:
                print('El grupo {}'.format(g))
                try:
                    pedir_orden_producto(sku, '3', recepcion, g)
                except:
                    pass
                try:
                    pedir_orden_producto2(sku, '3', recepcion, g)
                except:
                    pass
        elif diccionario[sku] < lotes_minimos_materia_prima_ajena * unidades_por_lote[sku]:
            for g in grupos:
                print('El grupo {}'.format(g))
                try:
                    pedir_orden_producto(sku, '3', recepcion, g)
                except:
                    pass
                try:
                    pedir_orden_producto2(sku, '3', recepcion, g)
                except:
                    pass


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
            if stock[sku] < delta_stock_minimo * stock_minimo[sku]:
                if fabricable(sku, stock):
                    preparar_despacho(recetas[sku])
                    print("Fabricando {}".format(nombres[sku]))
                    fabricar_producto(sku, unidades_por_lote[sku])
                else:
                    continue
        # Si no tenemos del producto, lo producimos
        else:
            if fabricable(sku, stock):
                preparar_despacho(recetas[sku])
                print("Fabricando {}".format(nombres[sku]))
                fabricar_producto(sku, unidades_por_lote[sku])
            else:
                continue

@shared_task
def despachar_pedido_bodega_smarter(sku, cantidad, almacenId):
    despachados = 0
    for i in range(2*int(cantidad)):
        sleep(1)
        producto = elegir_producto_a_despachar(sku)
        if not producto[0]:
            print("no hay producto")
            continue
        if not producto[1]:
            print('moviendo producto entre almacenes')
            mover_productos_entre_almacenes(producto[0]["_id"], despacho)
            if despachar_un_producto(producto[0]["_id"], almacenId, 10):
                despachados += 1
            if despachados == cantidad:
                return True
        else:
            print("intentando despachar")
            if despachar_un_producto(producto[0]["_id"], almacenId, 10):
                despachados += 1
            if despachados == cantidad:
                return True
    return False


def elegir_producto_a_despachar(sku):
    #primer elemento de la respuesta es el producto, el segundo es un boleand que es true si el producto esta en despahco, y false en caso contrario
    almacenes = obtener_almacenes_con_sku(sku)
    try:
        productos = json.loads(obtener_productos_en_almacen(despacho, sku))
        producto = random.choice(productos)
        respuesta = (producto, True)
        print('elegimos un producto para despachar')
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
            print('elegimoos un producto para despachar')
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
            if stock[sku] < delta_stock_minimo * stock_deseado_productos_intermedios[sku]:
                if fabricable(sku, stock):
                    preparar_despacho(recetas[sku])
                    print("Fabricando {}".format(nombres[sku]))
                    fabricar_producto(sku, unidades_por_lote[sku])
                else:
                    continue
        # Si no tenemos del producto, lo producimos
        else:
            if fabricable(sku, stock):
                preparar_despacho(recetas[sku])
                print("Fabricando {}".format(nombres[sku]))
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
            despachar_producto(producto['_id'], oc, direccion, precio)
            counter += 1
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
        posibilidad = revisar_posibilidad_entrega(pedido['id'])
        orden_compra = obtener_oc(pedido['id'])[0]
        delta = orden_compra['cantidad'] - orden_compra['cantidadDespachada']
        # Rechazo
        if posibilidad == 3:
            rechazar_oc(pedido['id'], 'Poco tiempo')
            borrar_archivo(pedido['archivo'])
        # Busco cocinar
        elif posibilidad == 2:
            cocinar(pedido['sku'], delta)
        # Busco crear sub
        elif posibilidad == 1:
            pass
        elif posibilidad == 0:
            aceptar_oc(pedido['id'])
            despachar_a_cliente(pedido['sku'], delta, 'b2c', 1000, pedido['id'])
            orden_compra = obtener_oc(pedido['id'])[0]
            delta_final = orden_compra['cantidad'] - orden_compra['cantidadDespachada']
            if delta_final <= 0:
                archivos_a_borrar.append(pedido['archivo'])
        borrar_archivo(archivos_a_borrar)
