from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from appdocs import views

admin.site.site_header = "Creación/Almacenamiento de Documentos del ECUAPASS"
admin.site.site_title  = "Creación/Almacenamiento de Documentos del ECUAPASS"
admin.site.index_title = "Creación/Almacenamiento de Documentos del ECUAPASS Admin"

urlpatterns = [
    #path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path("usuarios/", include("appusuarios.urls")),
    path("documentos/", include("appdocs.urls")),
    path("reportes/", include("appreportes.urls")),
]

