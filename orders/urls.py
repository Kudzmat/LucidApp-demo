from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'orders'
urlpatterns = [
    path('new-store-order', views.new_order, name='new_order'),
    path('view-orders', views.view_store_orders, name='view_orders'),
]