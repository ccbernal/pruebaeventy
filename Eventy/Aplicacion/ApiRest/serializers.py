from rest_framework.serializers import ModelSerializer, Serializer
from Aplicacion.models import Servicio, Actividad, Evento, Empresa, Informacion,\
     Asistente, Opcion, Pregunta, MuestraComercial, Memoria, Patrocinador, RutaAudio

class ServicioSerializer(ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id','nombre',)
        
class RutaAudioSerializer(ModelSerializer):
    class Meta:
        model = RutaAudio
        fields = ('id','idioma','url_android','url_ios')
        
class ActividadSerializer(ModelSerializer):
    
    class Meta:
        model = Actividad
        fields = ('id','tipo','nombre','persona','caracter','cupos','informacion','imagen','fecha_inicio','hora_inicio','hora_fin',)
        
class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('id','nombre','descripcion','logo')

class EventoSerializer(ModelSerializer):
    
    class Meta:
        model = Evento
        fields = ('id','nombre','tipo','empresa')
              
class InformacionSerializer(ModelSerializer):
    
    evento = EventoSerializer(many = False)
    
    class Meta:
        model = Informacion
        fields = ('evento','fecha_inicio','fecha_fin','logo','localizacion')
        
class AsistenteSerializer(ModelSerializer):
    
    class Meta:
        model = Asistente
        fields = ('id','nombre','apellido','celular','email','cargo','imagen','activo')
    
class OpcionSerializer(ModelSerializer):
    
    class Meta:
        model = Opcion
        fields = ('id', 'numeral', 'texto')
        
class PreguntaSerializer(ModelSerializer):
    
    opcion_set = OpcionSerializer(many = True)
    
    class Meta:
        model = Pregunta
        fields = ('id', 'texto', 'opcion_set')
        
class MuestraCSerializer(ModelSerializer):
    
    class Meta:
        model = MuestraComercial
        fields = ('id','nombre_empresa','logo','stand','hipervinculo','email')
        
class MemoriaSerializer(ModelSerializer):
    
    class Meta:
        model = Memoria
        fields = ('id','nombre','archivo','descripcion')
        
class ActividadMemoriaSerializer(ModelSerializer):
    
    memoria_set = MemoriaSerializer(many = True)
    
    class Meta:
        model = Actividad
        fields = ('id','nombre','memoria_set')

class PatrocinadorSerializer(ModelSerializer):
    
    class Meta:
        
        model = Patrocinador
        fields = ('id','nombre','baner','hipervinculo','logo')
        
        

        
        
        