#shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('compare/', views.compare_products, name='compare_products'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('product/<int:product_id>/image/', views.product_image, name='product_image'),
    path('search/', views.product_search, name='product_search'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('get-products-by-category/', views.get_products_by_category, name='get_products_by_category'),
]