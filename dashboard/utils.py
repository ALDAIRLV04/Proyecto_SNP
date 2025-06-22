from django.conf import settings
from django.core.mail import send_mail
from .models import Muestra, Alerta


def enviar_alertas(threshold=2):
    muestras = Muestra.objects.filter(nivel_riesgo__gte=threshold)
    for muestra in muestras:
        mensaje = f'Riesgo alto detectado en {muestra.nombre}'
        send_mail('Alerta BioSNP-Agua', mensaje, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        Alerta.objects.create(muestra=muestra, nivel_riesgo=muestra.nivel_riesgo, mensaje=mensaje)
