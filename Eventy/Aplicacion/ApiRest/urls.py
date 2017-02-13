from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from Aplicacion.ApiRest.views import obtener_actividades,\
    cambiar_hora, validar_asistente, obtener_eventos, obtener_datos,\
    obtener_asistentes, ingresar_evento_publico, validar_ingreso,\
    obtener_preguntas, registrar_voto, enviar_duda, obtener_datos_id,\
    editar_datos, obtener_empresas, obtener_asistentes_evento,\
    obtener_muestra_comercial, obtener_memorias, IngresarPuntoControl,\
    ingresar_punto_control, actividades_punto_control, escanear_asistente,\
    obtener_patrocinadores, obtener_ruta_audio

# router = DefaultRouter()
# router.register(r'grupos', GrupoViewSet)

urlpatterns = [
    url(r'^obtener_actividades/$', obtener_actividades),
    url(r'^cambiar_hora/$', cambiar_hora),
    url(r'^validar_asistente/$', validar_asistente),
    url(r'^obtener_eventos/$', obtener_eventos),
    url(r'^obtener_datos/$', obtener_datos),
    url(r'^obtener_asistentes/$', obtener_asistentes),
    url(r'^ingresar_evento_publico/$',ingresar_evento_publico),
    url(r'^validar_ingreso/$', validar_ingreso),
    url(r'^obtener_preguntas/$', obtener_preguntas),
    url(r'^registrar_voto/$', registrar_voto),
    url(r'^enviar_duda/$', enviar_duda),
    url(r'^obtener_datos_id/$', obtener_datos_id),
    url(r'^editar_datos/$', editar_datos),
    url(r'^obtener_empresas/$', obtener_empresas),
    url(r'^obtener_asistentes_evento/$', obtener_asistentes_evento),
    url(r'^obtener_muestra_comercial/$', obtener_muestra_comercial),
    url(r'^obtener_memorias/$', obtener_memorias),
    url(r'^ingresar_punto_control/$', ingresar_punto_control),
    url(r'^actividades_punto_control/$', actividades_punto_control),
    url(r'^escanear_asistente/$', escanear_asistente),
    url(r'^obtener_patrocinadores/$', obtener_patrocinadores),
    url(r'^obtener_ruta_audio/$', obtener_ruta_audio),
]
