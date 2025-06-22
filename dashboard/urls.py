from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path('reporte/pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('descargar_grafico/', views.descargar_grafico, name='descargar_grafico'),

]