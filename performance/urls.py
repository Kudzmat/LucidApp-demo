from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'performance'
urlpatterns = [
    path('monthly-performance/', views.view_monthly_performance, name='monthly_performance'),
]