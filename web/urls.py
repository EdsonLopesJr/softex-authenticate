from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.register, name='registro'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]

