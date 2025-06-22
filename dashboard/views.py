import base64
from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfgen import canvas

import matplotlib.pyplot as plt
from django.shortcuts import render
from django.utils.dateparse import parse_date

from .models import Muestra


def home(request):
    muestras = Muestra.objects.all()

    desde = parse_date(request.GET.get('desde') or "")
    hasta = parse_date(request.GET.get('hasta') or "")
    riesgo = request.GET.get('riesgo')

    if desde:
        muestras = muestras.filter(fecha__gte=desde)
    if hasta:
        muestras = muestras.filter(fecha__lte=hasta)
    if riesgo is not None:
        muestras = muestras.filter(nivel_riesgo__gte=int(riesgo))

    fig, ax = plt.subplots()
    colores = ['green', 'yellow', 'red']
    for muestra in muestras:
        color = colores[min(max(muestra.nivel_riesgo, 0), 2)]
        ax.scatter(muestra.longitud, muestra.latitud, color=color)
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.set_title('Ubicaciones de muestras')

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    image_png = buffer.getvalue()
    buffer.close()
    grafico = base64.b64encode(image_png).decode('utf-8')

    context = {
        'muestras': muestras,
        'grafico': grafico,
    }
    return render(request, 'dashboard/home.html', context)

def descargar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    
    p = canvas.Canvas(response)
    muestras = Muestra.objects.all()
    
    p.drawString(100, 800, "Reporte de Muestras")
    y = 780
    for muestra in muestras:
        p.drawString(100, y, f"{muestra.nombre} - {muestra.fecha} - Riesgo: {muestra.nivel_riesgo}")
        y -= 20

    p.showPage()
    p.save()
    return response

def descargar_grafico(request):
    muestras = Muestra.objects.all()

    fig, ax = plt.subplots()
    colores = ['green', 'yellow', 'red']
    for muestra in muestras:
        color = colores[min(max(muestra.nivel_riesgo, 0), 2)]
        ax.scatter(muestra.longitud, muestra.latitud, color=color)
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.set_title('Ubicaciones de muestras')

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    image_png = buffer.getvalue()
    buffer.close()

    response = HttpResponse(image_png, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="grafico_muestras.png"'
    return response
