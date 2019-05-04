from django.urls import path

from . import views

urlpatterns = [
    path('inventories', views.inventories, name='inventories'),
    path('orders', views.orders, name='orders'),
    path('inventories/', views.inventories, name='inventories'),
    path('orders/', views.orders, name='orders'),


    # Borrar urls despues
    path('', views.index, name='index'),
    path('skus_stock/', views.skus_stock, name='skus_stock'),
    path('productos_en_almacen/', views.productos_en_almacen, name='productos_en_almacen'),
    path('fabricar_sin_pagar/', views.fabricar_sin_pagar, name='frabricar_sin_pagar'),
    path('obtener_cuenta/', views.obtener_cuenta, name='obtener_cuenta'),
    path('obtener_eliminar_hook/', views.obtener_eliminar_hook, name='obtener_eliminar_hook'),
    path('obtener_obtener_hook/', views.obtener_obtener_hook, name='obtener_obtener_hook'),
    path('obtener_setear_hook/', views.obtener_setear_hook, name='obtener_setear_hook'),
]
