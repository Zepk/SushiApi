from celery import shared_task
import json
from .modules.funciones_bodega import *
from .modules.funciones_bodega_internos import *
import random
from time import sleep

# mueve periodicamente los productos de pulmon y recepcion a almacenes de proposito general
# Falta tomar en cuenta que no todos los productos son de tamano 1
@shared_task
def vaciar_recepcion_y_pulmon():
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

# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_propios():
    diccionario = contar_productos()
    for sku in skus_propios:
        if sku not in diccionario.keys():
            fabricar_producto(sku, str(unidades_por_lote[sku]))
        elif diccionario[sku] < lotes_minimos_materia_prima_propia * unidades_por_lote[sku]:
            fabricar_producto(sku, str(unidades_por_lote[sku]))
            print('pidiendo productos')


# De momento pide 1 lote de cada una de las materias primas que podemos producir, siempre que tengamos menos de 10 lotes
@shared_task
def pedir_productos_ajenos():
    diccionario = contar_productos()
    for sku, grupos in produccion_otros.items():
        print('El sku {}'.format(sku))
        if sku == '1013' and diccionario[sku] < delta_stock_minimo * stock_minimo[sku]:
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
        elif sku not in diccionario.keys():
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
def despachar_pedido_bodega(sku, cantidad, almacenId):
    almacenes = obtener_almacenes_con_sku(sku)
    despachados = 0
    for almacen in almacenes.keys():
        productos = json.loads(obtener_productos_en_almacen(almacen, sku))
        for producto in productos:
            if almacenes[almacen]["despacho"]:
                if despachar_un_producto(producto["_id"], almacenId, 10):
                    despachados += 1
            else:
                mover_productos_entre_almacenes(producto["_id"], despacho)
                if despachar_un_producto(producto["_id"], almacenId, 10):
                    despachados += 1
            if despachados == cantidad:
                return True
    return False


#Usar este en lugar del de arriba
@shared_task
def despachar_pedido_bodega_smart(sku, cantidad, almacenId):
    despachados = 0
    productos = json.loads(obtener_productos_en_almacen(despacho, sku))
    for producto in productos:
        if despachar_un_producto(producto["_id"], almacenId, 10):
            despachados += 1
        if despachados == cantidad:
            return True
    almacenes = obtener_almacenes_con_sku(sku)
    for almacen in almacenes.keys():
        if not almacenes[almacen]["despacho"]:
            productos = json.loads(obtener_productos_en_almacen(almacen, sku))
            for producto in productos:
                mover_productos_entre_almacenes(producto["_id"], despacho)
                if despachar_un_producto(producto["_id"], almacenId, 10):
                    despachados += 1
                if despachados == cantidad:
                    return True
    return False

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


