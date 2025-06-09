from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'orders'
urlpatterns = [
    path('restock-order', views.create_existing_item_order, name='new_existing_order'),
    path('new-inventory-order', views.create_new_item_order, name='new_order'),
    path('view-orders', views.view_store_orders, name='view_orders'),
    path('view-inventory', views.view_inventory, name='view_inventory'),
]