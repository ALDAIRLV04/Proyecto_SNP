import base64
from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfgen import canvas

import matplotlib.pyplot as plt
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.db.models import Count

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
    riesgos = {
        0: {'color': 'green', 'label': 'Bajo'},
        1: {'color': 'yellow', 'label': 'Medio'},
        2: {'color': 'red', 'label': 'Alto'},
    }
    coords = {0: {'x': [], 'y': []}, 1: {'x': [], 'y': []}, 2: {'x': [], 'y': []}}
    for muestra in muestras:
        nivel = max(0, min(muestra.nivel_riesgo, 2))
        coords[nivel]['x'].append(muestra.longitud)
        coords[nivel]['y'].append(muestra.latitud)
    for nivel, info in riesgos.items():
        if coords[nivel]['x']:
            ax.scatter(coords[nivel]['x'], coords[nivel]['y'],
                       color=info['color'], label=info['label'])
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.set_title('Ubicaciones de muestras')
    ax.legend(title='Nivel de riesgo')

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    image_png = buffer.getvalue()
    buffer.close()
    grafico = base64.b64encode(image_png).decode('utf-8')

    # Histograma de niveles de riesgo
    fig_h, ax_h = plt.subplots()
    niveles = [m.nivel_riesgo for m in muestras]
    ax_h.hist(niveles, bins=[-0.5, 0.5, 1.5, 2.5], rwidth=0.8,
              color='skyblue', label='Muestras')
    ax_h.set_xticks([0, 1, 2])
    ax_h.set_xlabel('Nivel de riesgo')
    ax_h.set_ylabel('Cantidad')
    ax_h.set_title('Distribuci\u00f3n de Riesgos')
    ax_h.legend()
    buffer = BytesIO()
    fig_h.savefig(buffer, format='png')
    plt.close(fig_h)
    hist_png = buffer.getvalue()
    buffer.close()
    histograma = base64.b64encode(hist_png).decode('utf-8')

    # Evoluci\u00f3n temporal de riesgos (conteo por fecha)
    fig_l, ax_l = plt.subplots()
    fechas = list(muestras.order_by('fecha').values_list('fecha', flat=True).distinct())
    conteos = [muestras.filter(fecha=f).count() for f in fechas]
    ax_l.plot(fechas, conteos, marker='o', label='Muestras')
    ax_l.set_xlabel('Fecha')
    ax_l.set_ylabel('Muestras')
    ax_l.set_title('Evoluci\u00f3n Temporal')
    ax_l.legend()
    buffer = BytesIO()
    fig_l.autofmt_xdate()
    fig_l.savefig(buffer, format='png')
    plt.close(fig_l)
    line_png = buffer.getvalue()
    buffer.close()
    linea = base64.b64encode(line_png).decode('utf-8')

    # M\u00e9tricas de resumen
    total = muestras.count()
    altos = muestras.filter(nivel_riesgo__gte=2).count()
    porcentaje_altos = (altos / total * 100) if total else 0
    ultima_muestra = muestras.order_by('-fecha').first()
    ultima_fecha = ultima_muestra.fecha if ultima_muestra else None

    context = {
        'muestras': muestras,
        'grafico': grafico,
        'histograma': histograma,
        'linea': linea,
        'total_muestras': total,
        'porcentaje_altos': porcentaje_altos,
        'fecha_ultima_muestra': ultima_fecha,
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
