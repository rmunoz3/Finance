from rest_framework import serializers
from .models import Accion

class accionesSerializer (serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = ['ticker','fecha','precio_apertura','precio_cierre','volumen']