

from django.db import models

class Accion(models.Model):
    ticker = models.CharField(max_length=10)
    fecha = models.DateField()
    precio_apertura = models.DecimalField(max_digits=10, decimal_places=2)
    precio_cierre = models.DecimalField(max_digits=10, decimal_places=2)
    volumen = models.IntegerField()

    def __str__(self):
        return self.ticker
