from django.http import JsonResponse
from .models import Accion
from .serializers import accionesSerializer
import requests
from django.shortcuts import render
from datetime import datetime
import io
import urllib
import base64
import matplotlib.pyplot as plt

def convertir_fecha(fecha_en_milisegundos):
    return datetime.fromtimestamp(fecha_en_milisegundos / 1000).date()
    # //este codigo lo que hace es convertir la fecha en milisegundos a una fecha normal usando la libreria datetime


def obtener_datos_accion(ticker, fecha_inicio, fecha_fin, clave_api):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}?apiKey={clave_api}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Respuesta JSON:", response.json())  # Imprime la respuesta aquí
        return response.json()
    else:
        print("Error en la respuesta de la API:", response.status_code)
        return None


def guardar_datos_accion(ticker, datos_accion):
    for dato in datos_accion['results']:
        accion = Accion(
            ticker=ticker,  # Usa el ticker proporcionado por el usuario
            fecha=convertir_fecha(dato['t']),
            precio_apertura=dato['o'],
            precio_cierre=dato['c'],
            volumen=dato['v']
        )
        accion.save()

def vista_acciones(request):
    mensaje = ''
    if request.method == 'POST':

        ticker = request.POST.get('ticker')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        clave_api = 'wR1pfwA0RItse1cOC3Av8n4cTiiZN37e'  # Reemplaza con tu clave API real

        datos_accion = obtener_datos_accion(ticker, fecha_inicio, fecha_fin, clave_api)
        if datos_accion:
            guardar_datos_accion(ticker, datos_accion)  # Pasa el ticker aquí
            mensaje = 'Datos guardados correctamente'
        else:
            mensaje = 'No se pudieron obtener datos'

    return render(request, 'myappfinanciera/formulario.html', {'mensaje': mensaje})




def visualizar_datos(request):
    # Obtener datos de la base de datos
    ticker = request.GET.get('ticker', None)  # Usa 'None' como valor por defecto si 'ticker' no está presente

    acciones = Accion.objects.filter(ticker=ticker)

    # Preparar los datos para el gráfico
    fechas = [accion.fecha for accion in acciones]
    precios_cierre = [accion.precio_cierre for accion in acciones]

    # Crear un gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, precios_cierre, marker='o')
    plt.title(f"Precio de Cierre de {ticker} a lo Largo del Tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Precio de Cierre")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Convertir el gráfico a PNG
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    string = base64.b64encode(buffer.read())
    uri = urllib.parse.quote(string)
    
    # Renderizar la respuesta
    return render(request, 'myappfinanciera/visualizacion.html', {'grafico': uri})

