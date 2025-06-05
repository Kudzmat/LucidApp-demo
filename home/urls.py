from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', LogoutView.as_view(next_page='home:sign_in'), name='logout'),  # Redirect to sign-in after logout
]