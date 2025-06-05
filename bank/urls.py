from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'bank'
urlpatterns = [
    path('withdraw', views.withdrawal, name='withdrawal'),
    path('deposit', views.deposit, name='deposit'),
    path('statement', views.view_statement, name='statement'),
]