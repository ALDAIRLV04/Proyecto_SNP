from django.db import models


class Muestra(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    nivel_riesgo = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class ResultadoAnalisis(models.Model):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    genes_detectados = models.TextField(blank=True)

    def __str__(self):
        return f"Resultado de {self.muestra.nombre}"


class Alerta(models.Model):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE)
    nivel_riesgo = models.IntegerField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta {self.nivel_riesgo} - {self.muestra.nombre}"