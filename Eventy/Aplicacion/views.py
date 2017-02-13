from django.shortcuts import render
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.highcharts import ColumnChart
from Aplicacion.models import Pregunta, Opcion, Evento, PuntoControl, Actividad

def index(request):

    pregunta = Pregunta.objects.get(id = request.GET.get("id_pregunta"))
    print (pregunta)
    datos = [['texto' , 'votos']]
    
    opciones = Opcion.objects.filter(pregunta__id = pregunta.id)
    print (opciones)
        
    for opcion in opciones:
        values = []
        values.append(opcion.texto)
        values.append(opcion.votos)
        datos.append(values)           
        
    chart = ColumnChart(SimpleDataSource(data=datos), options={'title': pregunta.texto})
    
    context = {'chart': chart,'pregunta': pregunta,'usuario': request.user}
    return render(request, 'grafica/index.html', context)

def estadistica(request):

    evento = Evento.objects.get(id = request.GET.get("id_evento"))
    
    asistentes = evento.asistente_set.all()
    print (asistentes)
    datos = [['genero' , 'Numero de Asistentes']]
    masc = 0
    fem = 0
        
    for asistente in asistentes:
        if asistente.genero == 'Masculino':
            masc = masc + 1
        else:
            fem = fem + 1
    
    valuesM = []
    valuesM.append('Masculino')
    valuesM.append(masc)
    datos.append(valuesM)   
    
    valuesF = []
    valuesF.append('Femenino')
    valuesF.append(fem)
    datos.append(valuesF)   
            
    chart = ColumnChart(SimpleDataSource(data=datos), options={'title': evento.nombre})
    
    context = {'chart': chart,'evento': evento,'usuario': request.user}
    return render(request, 'estadisticas/estadistica.html', context)

def validar_asistentes(request):

    if request.user.is_superuser:
        actividades = Actividad.objects.all()
        
    else:
        punto_control = PuntoControl.objects.get(usuario__id = request.user.id)
        actividades =  punto_control.actividades.all()
        
    context = {'usuario': request.user,'actividades':actividades}
    return render(request, 'validar_asistentes/validar_asistentes.html', context)

def datos_validados(request):
    print request.POST
    punto_control = PuntoControl.objects.get(usuario__id = request.user.id)
    actividades =  punto_control.actividades.all()
    context = {'usuario': request.user,'actividades':actividades}
    return render(request, 'validar_asistentes/validar_asistentes.html', context)
# Create your views here.
