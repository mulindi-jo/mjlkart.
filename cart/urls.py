from django.urls import path

from cart import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<str:product_id>/', views.add_product_item_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:product_id>/', views.remove_product_item_from_cart, name='remove_from_cart'),
    path('remove_product_from_cart/<str:product_id>/', views.remove_product_from_cart, name='remove_product_from_cart')
]
