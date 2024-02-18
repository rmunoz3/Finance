# MisFinanzasApp/urls.py

from django.urls import path
from . import views
# //antes de acceder a estos urls especificos django busca los urls del proyecto
urlpatterns = [
    path('', views.vista_acciones ,name='vista_acciones'),
    path('visualizar/', views.visualizar_datos, name='visualizar_datos'),
]
