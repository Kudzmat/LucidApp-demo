from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'sales'
urlpatterns = [
    path('new-store-sale', views.new_sale, name='new_sale'),
    path('new-online-sale', views.new_online_sale, name='new_online_sale'),
]