from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('skus_stock/', views.skus_stock, name='skus_stock'),
    path('productos_en_almacen/', views.productos_en_almacen, name='productos_en_almacen'),
    path('fabricar_sin_pagar/', views.fabricar_sin_pagar, name='frabricar_sin_pagar'),
    path('obtener_cuenta/', views.obtener_cuenta, name='obtener_cuenta'),
]
