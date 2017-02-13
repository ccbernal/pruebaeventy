from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Aplicacion.ApiRest.serializers import ServicioSerializer,\
    ActividadSerializer, InformacionSerializer,\
    AsistenteSerializer, PreguntaSerializer, EmpresaSerializer,\
    MuestraCSerializer,ActividadMemoriaSerializer, PatrocinadorSerializer, RutaAudioSerializer
from Aplicacion.models import Evento, Actividad, Informacion,\
    Asistente, Asistente_Ingresado, Opcion, Duda, Empresa, MuestraComercial,\
    PuntoControl, RutaAudio
    
from django.contrib.auth import authenticate


class ObtenerEventos(APIView):
    serializer_info = InformacionSerializer
    
    def get(self, request):
       
        info = Informacion.objects.all()
        
        if (len(info) > 0):
          
            respuesta = self.serializer_info(info, many = True, context = {"request" : request})
            return Response(respuesta.data, status = status.HTTP_200_OK)
        
        else:
            return Response({"mensaje":"No hay eventos para mostrar"}, status = status.HTTP_400_BAD_REQUEST)
        
obtener_eventos= ObtenerEventos.as_view()
        
class ObtenerActividades(APIView):
    serializer_class = ActividadSerializer
    
    def post(self,request):
        if request.data:
            evento = Evento.objects.get(id = request.data["id_evento"])
            actividades = evento.actividad_set.all()
            response = self.serializer_class(actividades, many = True)
            return Response(response.data, status=status.HTTP_200_OK)
            
        else:
            return Response({"mensaje": "No hay informacion"}, status=status.HTTP_400_BAD_REQUEST)
    
obtener_actividades = ObtenerActividades.as_view()       

class CambiarHora(APIView):
    
    def post(self, request):
        if request.data:
            actividad = Actividad.objects.get(id = request.data['actividad_id'])
            actividad.hora_inicio = request.data['hora_inicio']
            actividad.hora_fin = request.data['hora_fin']
            actividad.save()
            return Response({"mensaje":"Horas modificadas"}, status = status.HTTP_200_OK)
        else:
            return Response({"mensaje":"No hay informacion suficiente"}, status = status.HTTP_400_BAD_REQUEST)
        
cambiar_hora = CambiarHora.as_view()

class ValidarAsistente(APIView):
    
    def post(self, request):
        
        if (request.data):
            print ("entro")
            asistente = Asistente.objects.filter(celular = request.data['celular'])
            
            if(len(asistente) > 0):
                print asistente
                
                if (asistente[0].activo == True):
                    flag = Asistente_Ingresado.objects.filter(actividad__id = request.data['id_actividad'], asistente__id = asistente[0].id)
                    
                    if (len(flag) == 0):
                        actividad = Actividad.objects.filter(id = request.data['id_actividad'])[0]
                        flag = Asistente_Ingresado.create(asistente[0], actividad, True)
                        return Response({"mensaje": 1}, status = status.HTTP_200_OK)
                    else:
                        flag[0].ingresado = True
                        flag[0].save()
                        return Response({"mensaje":2}, status =status.HTTP_200_OK)
                else:
                    return Response({"mensaje":4}, status = status.HTTP_200_OK)
            else:
                return Response({"mensaje":3}, status = status.HTTP_200_OK)
        else:
            return Response({"mensaje":"Falta el id de la actividad y el asistente"}, status = status.HTTP_400_BAD_REQUEST)
        
validar_asistente = ValidarAsistente.as_view()

class ObtenerAsistentes(APIView):
    serializer_class = AsistenteSerializer
    
    def post(self, request):
        
        if request.data:
            ingresados = Asistente_Ingresado.objects.filter(actividad__id = request.data['id_actividad'])
            asistentes = []
            
            if(len(ingresados)>0):
                for ingresado in ingresados:
                    asistentes.append(ingresado.asistente)
            
            respuesta = self.serializer_class(asistentes, many = True)
            return Response(respuesta.data, status = status.HTTP_200_OK)   
        else:
            return Response({"mensaje":"No se suministro el id de la actividad"}, status = status.HTTP_400_BAD_REQUEST)  
        
obtener_asistentes = ObtenerAsistentes.as_view() 

class ObtenerDatos(APIView):
    
    serializer_asistente = AsistenteSerializer
    
    def post(self, request):
        if (request.data):
            asistente = Asistente.objects.filter(celular = request.data['celular'])
            print asistente[0]
            
            if(len(asistente) > 0):
                respuesta = self.serializer_asistente(asistente[0], many = False)
                return Response(respuesta.data, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No hay asistente registrado con ese numero de celular"}, status = status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({"mensaje":"No se suministro numero de celular"}, status = status.HTTP_400_BAD_REQUEST)

obtener_datos = ObtenerDatos.as_view()     


class IngresarEventoPublico(APIView):
    
    def post(self, request):
        
        if request.data:
            evento = Evento.objects.filter(id = request.data['id_evento'])
            
            if (len(evento) > 0):
                asistente = Asistente.create('asistente', 'asistente', '5000000000', 'asistente', 'blank','Masculino')
                asistente.eventos.add(evento[0])
                actividades = evento[0].actividad_set.all()
                
                if (len(actividades) >0):
                    for actividad in actividades:
                        asistente.actividades.add(actividad)
                        
                return Response({"mensaje":"Asistente registrado"}, status = status.HTTP_200_OK)
            else:
                return Response({"mensaje":"No se encontro un evento con ese id"}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({"mensaje":"No se ha suministrado informacion para la consulta"}, status=status.HTTP_400_BAD_REQUEST)
        
ingresar_evento_publico = IngresarEventoPublico.as_view()


class ValidarIngreso(APIView):
    
    def post(self, request):
        
        if request.data:
            
            asistente = Asistente.objects.filter(id = request.data['id_asistente'])
            
            if ( len(asistente) > 0 ):
                
                if ( len(asistente[0].actividades.all().filter(id = request.data['id_actividad'])) > 0):
                    
                    return Response({"mensaje":"El asistente esta autorizado para ingresar"}, status = status.HTTP_200_OK)
                    
                else:
                    return Response({"mensaje":"El asistente no tiene permiso para ingresar"}, status = status.HTTP_403_FORBIDDEN)
                
            else:
                return Response({"mensaje":"No se encontro un asistente con el ID suministrado"}, status = status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status = status.HTTP_400_BAD_REQUEST)

validar_ingreso = ValidarIngreso.as_view()

class ObtenerPreguntas(APIView):
    
    serializer_pregunta = PreguntaSerializer
    
    def post(self, request):
        
        if request.data:
            
            actividad = Actividad.objects.filter(id = request.data['id_actividad'])
            
            if (len(actividad) > 0):
                
                preguntas = actividad[0].pregunta_set.all()
                respuesta = self.serializer_pregunta(preguntas, many = True)
                return Response(respuesta.data, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro una actividad con el id suministrado"}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros necesarios"}, status=status.HTTP_400_BAD_REQUEST)

obtener_preguntas = ObtenerPreguntas.as_view()

class RegistrarVoto(APIView):
    
    def post(self, request):
        
        if request.data:
            
            opcion = Opcion.objects.filter(id = request.data['id_opcion'])
            
            if (len(opcion) > 0):
                
                opcion[0].votos = opcion[0].votos + 1
                opcion[0].save()
                
                return Response({"mensaje":"Se ha registrado el voto"}, status=status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro la opcion con el id suministrado"}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros necesarios"}, status=status.HTTP_400_BAD_REQUEST)
        
registrar_voto = RegistrarVoto.as_view()

class EnviarDuda(APIView):
    
    def post(self, request):
        
        if request.data:
            asistente = Asistente.objects.filter(id = request.data['id_asistente'])
            actividad = Actividad.objects.filter(id = request.data['id_actividad'])
            
            if(len(asistente)>0 and len(actividad)>0):
                
                texto = request.data['texto']
                Duda.create(texto, actividad[0], asistente[0])
                
                return Response({"mensaje":"Duda registrada con exito"}, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro el asistente o actividad con el id suminstrado"}, status = status.HTTP_404_NOT_FOUND)
            
        else:
            
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
                
enviar_duda = EnviarDuda.as_view()


class ObtenerDatosId(APIView):
    
    serializer_asistente = AsistenteSerializer
    
    def post(self, request):
        
        if request.data:
            
            asistente = Asistente.objects.filter(id = request.data['id_asistente'])
            
            if ( len(asistente) > 0):
                
                respuesta = self.serializer_asistente(asistente[0], many = False)
                
                return Response(respuesta.data, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro un asistente con el id suministrado"}, status = status.HTTP_404_NOT_FOUND)
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)

obtener_datos_id = ObtenerDatosId.as_view()

class EditarDatos(APIView):
    
    def post(self, request):
        
        if request.data:
            
            asistente = Asistente.objects.filter(id = request.data['id_asistente'])
            
            if (len(asistente) >0):
                
                asistente[0].nombre = request.data['nombre']
                asistente[0].apellido = request.data['apellido']
                asistente[0].email = request.data['email']
                asistente[0].cargo = request.data['cargo'];
                asistente[0].foto = request.data['foto']
                asistente[0].empresa = Empresa.objects.get(id = request.data['id_empresa'])
                asistente[0].save()
                
                return Response({"mensaje":"Se han actualizado los datos con exito"}, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro un asistente con el id suministrado"}, status = status.HTTP_404_NOT_FOUND) 
            
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        
editar_datos = EditarDatos.as_view()
            

class ObtenerEmpresas(APIView):
    
    serializer_empresas = EmpresaSerializer
    
    def post(self, request):
        
        if request.data:
            
            empresas = Empresa.objects.filter(evento__id = request.data['id_evento'])
            respuesta = self.serializer_empresas(empresas, many = True)
            return Response(respuesta.data, status = status.HTTP_200_OK)
            
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        
obtener_empresas = ObtenerEmpresas.as_view()


class ObtenerAsistentesEvento(APIView):
    
    serializer_asistente = AsistenteSerializer
    
    def post(self, request):
        
        if request.data:
            
            asistentes = Asistente.objects.filter(eventos__id = request.data['id_evento'], activo = True)
            respuesta = self.serializer_asistente(asistentes, many = True)
            
            return Response(respuesta.data, status = status.HTTP_200_OK)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
       
obtener_asistentes_evento = ObtenerAsistentesEvento.as_view() 


class ObtenerMuestraComercial(APIView):
    
    serializer_muestra = MuestraCSerializer
    
    def post(self, request):
        
        if request.data:
            
            muestras = MuestraComercial.objects.filter(evento__id = request.data['id_evento'])
            
            respuesta = self.serializer_muestra(muestras, many = True)
            
            return Response(respuesta.data, status = status.HTTP_200_OK)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST) 
        
obtener_muestra_comercial = ObtenerMuestraComercial.as_view()


class ObtenerMemorias(APIView):
    
    serializer_actividad = ActividadMemoriaSerializer
    
    def post(self, request):
        
        if request.data:
            
            actividades = Actividad.objects.filter(evento__id = request.data['id_evento'])
            
            respuesta = self.serializer_actividad(actividades, many = True)
            
            return Response(respuesta.data, status = status.HTTP_200_OK)
        
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
       
obtener_memorias = ObtenerMemorias.as_view() 
            
      
class IngresarPuntoControl(APIView):
    
    def post(self, request):
        
        if (request.data):
            
            usuario = authenticate(username = request.data['usuario'], password = request.data['clave'])
            
            if (usuario != None):
                punto_control = PuntoControl.objects.filter(usuario__id = usuario.id)
                
                if ( len(punto_control)>0 ):
                    return Response({"mensaje":"Bienvenido","id_punto_control":punto_control[0].id}, status = status.HTTP_200_OK)
                
                else:
                    return Response({"mensaje":"No existe un punto de control asociado al usuario"}, status = status.HTTP_401_UNAUTHORIZED)
            
            else:
                return Response({"mensaje":"Usuario o clave incorrecta"}, status =status.HTTP_404_NOT_FOUND)
            
        else:
            
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
            
                
ingresar_punto_control = IngresarPuntoControl.as_view()
    

class ActividadesPuntoControl(APIView):
    
    serializer_class = ActividadSerializer
    
    def post(self, request):
        
        if request.data:
            
            punto_control = PuntoControl.objects.filter(id = request.data['id_punto_control'])
            
            if (len(punto_control)>0):
                
                actividades = punto_control[0].actividades
                respuesta = self.serializer_class(actividades, many = True)
                
                return Response(respuesta.data, status = status.HTTP_200_OK)
            
            else:
                return Response({"mensaje":"No se encontro un punto de control con ese ID"}, status = status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status=status.HTTP_400_BAD_REQUEST)
            
actividades_punto_control = ActividadesPuntoControl.as_view()


class EscanearAsistente(APIView):
    
    def post(self, request):
        
        if (request.data):
            
            asistente = Asistente.objects.filter(celular = request.data['celular'])

            if(len(asistente) > 0):
                
                if (asistente[0].activo == True):
                    
                    actividad_registrada = asistente[0].actividades.filter(id = request.data['id_actividad'])
                    
                    if (len(actividad_registrada)>0):
                        
                        flag = Asistente_Ingresado.objects.filter(actividad__id = request.data['id_actividad'], asistente__id = asistente[0].id)
                        
                        if (len(flag) == 0):
                            actividad = actividad_registrada[0]
                            validado = Asistente_Ingresado.create(asistente[0], actividad, True)
                            return Response({"mensaje": "Asistente ingresado exitosamente"}, status = status.HTTP_200_OK)
                        else:
                            flag[0].ingresado = True
                            flag[0].save()
                            return Response({"mensaje":"El asistente ya habia ingresado a esta actividad"}, status = status.HTTP_200_OK)
                    else:
                        return Response({"mensaje":"El asistente no esta habilitado para ingresar a esta actividad"}, status = status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"mensaje":"El asistente no se encuentra activo"}, status = status.HTTP_403_FORBIDDEN)
            else:
                return Response({"mensaje":"No se encontro un asistente con el numero de celular proporcionado"}, status = status.HTTP_404_NOT_FOUND)
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status = status.HTTP_400_BAD_REQUEST)
        
escanear_asistente = EscanearAsistente.as_view()


class ObtenerPatrocinadores(APIView):
    
    serializer_class = PatrocinadorSerializer
    
    def post(self, request):
        
        if (request.data):
            
            info_evento = Informacion.objects.filter(evento__id = request.data['id_evento'])
            
            if ( len(info_evento)>0 ):
                
                patrocinadores = info_evento[0].patrocinadores.all()
                respuesta = self.serializer_class(patrocinadores, many = True)
                return Response(respuesta.data, status = status.HTTP_200_OK)
            
            else:
                
                return Response({"mensaje":"No se encontro evento con el id suministrado"}, status = status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status = status.HTTP_400_BAD_REQUEST)
                
                
obtener_patrocinadores = ObtenerPatrocinadores.as_view()

class ObtenerRutaAudio(APIView):

    serializer_class = RutaAudioSerializer
            
    def post(self, request):

        if request.data:

            rutas = RutaAudio.objects.filter(actividad__id = request.data['id_actividad'])
            respuesta = self.serializer_class(rutas, many = True)
            return Response(respuesta.data, status = status.HTTP_200_OK)

        else:
            return Response({"mensaje":"No se suministraron los parametros requeridos"}, status = status.HTTP_400_BAD_REQUEST)

obtener_ruta_audio = ObtenerRutaAudio.as_view()