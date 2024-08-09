#admin_panel/urls.py
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),  # Changed from 'orders' to 'order_list'
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('service-requests/', views.ServiceRequestListView.as_view(), name='service_request_list'),
    path('service-requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service_request_detail'),
    path('service-requests/<int:pk>/update/', views.ServiceRequestUpdateView.as_view(), name='service_request_update'),
    path('service-requests/<int:pk>/delete/', views.ServiceRequestDeleteView.as_view(), name='service_request_delete'),
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('reports/', views.reports, name='reports'),
    path('order-map/', views.order_map, name='order_map'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('settings/users/', views.user_management, name='user_management'),
    path('settings/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('chat/', views.admin_chat_list, name='admin_chat_list'),
    path('chat/<int:session_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('chat/<int:session_id>/send/', views.admin_send_message, name='admin_send_message'),
    path('chat/<int:session_id>/get/', views.admin_get_messages, name='admin_get_messages'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]