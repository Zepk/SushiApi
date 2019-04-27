from django.urls import path

from . import views

urlpatterns = [
    path('inventories/', views.inventories, name='inventories'),
    path('orders/', views.orders, name='orders'),
    # Borrar urls despues
    path('moveStock/', views.moveStock, name='moveStock'),
    path('moveStockBodega/', views.moveStockBodega, name='moveStockBodega'),
    path('almacenes/', views.almacenes, name='almacenes'),
    path('stockAlmacen/', views.stockAlmacen, name='stockAlmacen'),
    path('skusWithStock/', views.skusWithStock, name='skusWithStock'),
    path('fabrica/fabricarSinPago/', views.fabricarSinPago, name='fabricarSinPago'),
    path('fabrica/getCuenta/', views.getCuenta, name='getCuenta'),
    path('eliminarhook/', views.eliminarhook, name='eliminarhook'),
    path('obtenerhook/', views.obtenerhook, name='obtenerhook'),
    path('setearhook/', views.setearhook, name='setearhook'),
]
