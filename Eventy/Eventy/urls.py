"""Eventy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from Aplicacion.views import index, estadistica, validar_asistentes,\
    datos_validados
from django.conf import settings

urlpatterns = [
    url(r'^admin/Aplicacion/pregunta/grafica/',index),
    url(r'^admin/Aplicacion/evento/estadisticas/',estadistica),
    url(r'^admin/Aplicacion/validarasistente/',validar_asistentes),
    url(r'^datos_validados/',datos_validados),
    url(r'^admin/', admin.site.urls),
    url(r'^', admin.site.urls),
    url(r'^', include('Aplicacion.ApiRest.urls')),
    url(r'^chaining', include('smart_selects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
    
    
    
    
