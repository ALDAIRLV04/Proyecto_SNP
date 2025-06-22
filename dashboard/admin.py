from django.contrib import admin
from .models import Muestra, ResultadoAnalisis, Alerta


@admin.register(Muestra)
class MuestraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'latitud', 'longitud', 'nivel_riesgo')


@admin.register(ResultadoAnalisis)
class ResultadoAnalisisAdmin(admin.ModelAdmin):
    list_display = ('muestra', 'descripcion', 'genes_detectados')


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('muestra', 'nivel_riesgo', 'fecha_envio')