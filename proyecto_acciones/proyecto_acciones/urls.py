
from django.contrib import admin
from django.urls import path, include
from proyecto_acciones import views 
# //aqui se especifican las urls de todo el proyecto
urlpatterns = [
    path('', include('myappfinanciera.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('acciones/', include('myappfinanciera.urls')),  
]
