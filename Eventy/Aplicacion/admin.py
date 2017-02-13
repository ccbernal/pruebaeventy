from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import User,UserAdmin
from Aplicacion.models import Evento, Servicio, Actividad, Categoria, Asistente,\
    Empresa, Patrocinador, Memoria, MuestraComercial, PuntoControl, Pregunta,\
    Opcion, Duda, Informacion, Perfil, Asistente_Ingresado, RutaAudio
from django.contrib.auth.models import Permission
from django import forms
from django.forms.models import BaseInlineFormSet
from django.template.context_processors import request

admin.site.site_header = "Eventy"
admin.site.site_title = "Eventy"

class RequiredInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        if i < 1:
            form.empty_permitted = False
        return form
    
class PerfilForm(forms.ModelForm):
    
    class Meta:
        model = Perfil
        fields = ['rol','evento']
        
    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        
        if(self.current_user.is_superuser):
            qs = Evento.objects.all()
            
        else:
            qs = Evento.objects.filter(id = self.current_user.perfil.evento.id)
        self.fields['evento'].queryset = qs

class PerfilInline(admin.TabularInline):
    model = Perfil
    can_delete = False
    fields = ('rol','evento')
    form = PerfilForm
    formset = RequiredInlineFormSet

    
    def get_extra(self, request, obj=None, **kwargs):
        """Hook for customizing the number of extra inline forms."""
        self.form.current_user = request.user
        return self.extra

    
    
class UsuarioAdmin(UserAdmin):
    inlines = (PerfilInline,)
    
    def save_model(self, request, obj, form, change):
        obj.is_staff = 1
        obj.save()
        
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        print instances
        for instance in instances:
            usuario = instance.usuario
            permisos = []
            
            if (instance.rol == 1):
                # Usuario Administrador de evento
                permisos = Permission.objects.filter(codename__in = ("add_user","change_user","add_actividad","change_actividad",
                                                                     "delete_actividad","add_memoria","change_memoria","delete_memoria",
                                                                     "add_asistente","change_asistente","delete_asistente","add_empresa",
                                                                     "change_empresa","delete_empresa","add_informacion","change_informacion",
                                                                     "delete_informacion","add_patrocinador","change_patrocinador","delete_patrocinador",
                                                                     "add_muestracomercial","change_muestracomercial","delete_muestracomercial","add_puntocontrol",
                                                                     "change_puntocontrol","delete_puntocontrol","change_perfil"))
            if (instance.rol == 2):
                # Usuario de Soporte Tecnico
                permisos = Permission.objects.filter(codename__in = ("change_duda","delete_duda","add_pregunta","change_pregunta",
                                                                     "delete_pregunta","add_opcion","change_opcion","delete_opcion",
                                                                     "change_avanceagenda"))

            if (instance.rol == 3):
                # Usuario de Punto de Control
                permisos = Permission.objects.filter(codename = "change_validarasistente")
            
            usuario.user_permissions.set(permisos)
            
            if(request.user.is_superuser == False):
                instance.evento = request.user.perfil.evento
            
            instance.save()
        formset.save_m2m()

class EventoAdminView(admin.ModelAdmin):
    list_display = ('id', 'nombre','empresa','usuario_administrador', 'tipo','ver_estadisticas')
    filter_horizontal =  ('servicios',)
    ordering = ('id',)
    fieldsets = ( 
        ("Datos principales", { 'fields': ('nombre','empresa','tipo')}), 
        ("Servicios contratados", { 'fields': ('servicios',)}), 
    )
          
    def usuario_administrador(self, evento):
        admins = Perfil.objects.filter(evento__id = evento.id, rol = 1)
        nombres = ""
        
        for admin in admins:
            nombres = nombres + "<li>" + admin.usuario.username + "</li>"
        
        nombres = "<ul>"+nombres+"</ul>"
        return format_html(nombres)
    
    def ver_estadisticas(self, evento):
        return format_html("<a href='/admin/Aplicacion/evento/estadisticas/?id_evento={0}' target='_self'> <input type='button' id='{0}' value='Estadisticas' class='default estadistica' style='height:22px;width: 90px;padding:1px 1px;'></a>", evento.id)
    
    
class ServicioAdminView(admin.ModelAdmin):
    list_display = ('id', 'nombre','descripcion',)
    fieldsets = ( 
        ("Datos principales", { 'fields': ('nombre','descripcion',)}), 
    )

def cambiar_estado(modeladmin, request, asistentes):
    for asistente in asistentes:
        
        if (asistente.activo == True):
            asistente.activo = False
            asistente.save()
        else:
            asistente.activo = True
            asistente.save()

cambiar_estado.short_description = "Activar/Desactivar Asistentes"
 

class AsistenteForm(forms.ModelForm):
    
    class Meta:
        model = Asistente
        fields = ['categoria','nombre', 'eventos','apellido','genero', 'celular','email','activo','empresa', 'cargo','actividades']
        
    def __init__(self, *args, **kwargs):
        super(AsistenteForm, self).__init__(*args, **kwargs)
        
        if self.current_user.is_superuser:
            self.fields['actividades'].queryset = Actividad.objects.all()
        else:
            self.fields['actividades'].queryset = self.current_user.perfil.evento.actividad_set.all()
       
        
class AsistenteAdminView(admin.ModelAdmin):
        
    campos_normaluser =  ( 
        ("Datos Personales", { 'fields': ('categoria','nombre', 'apellido','genero', 'celular','email','activo')}), 
        ("Trabajo", { 'fields': ('empresa', 'cargo',)}),
        ("Permisos", { 'fields': ('actividades',)}),
    )
    
    campos_superuser = (
                        ("Eventos", { 'fields': ('eventos',)}),
                        )
    
    list_display = ('id','nombre', 'apellido', 'celular','email','empresa','cargo','activo')
    ordering = ('id',)
    raw_id_fields = ("empresa", )
    list_filter = (('actividades', admin.RelatedOnlyFieldListFilter),('eventos', admin.RelatedOnlyFieldListFilter),)
    filter_horizontal = ('actividades','eventos')
    actions = [cambiar_estado]
    search_fields = ('nombre', 'celular')
    form = AsistenteForm
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(AsistenteAdminView, self).get_form(request, obj, **kwargs)
                
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        
        if request.user.is_superuser:
            obj.save()
            
        else:
            
            if (change != 1):
                buscado = Asistente.objects.filter(celular = obj.celular)
            
                if(len(buscado) >0):
                    obj.id = buscado[0].id
                    obj.eventos.add(request.user.perfil.evento)
                    
                else:
                    obj.save()
                    obj.eventos.add(request.user.perfil.evento)
            else:
                obj.save()
        
        
    def get_queryset(self, request):
        qs = super(AsistenteAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventos__id=request.user.perfil.evento.id)
   
class ValidarAsistente(Asistente):
        
    class Meta:
        proxy = True

class ValidarAsistenteAdmin(AsistenteAdminView):
    class Media:
        js = ('js/owner/validarAsistentes.js','js/jquery/jquery.cookie.js')
        
    list_display = ('id','nombre', 'apellido', 'celular','email','empresa','cargo','activo')
    list_filter = (('actividades', admin.RelatedOnlyFieldListFilter),)
    actions = None
    list_display_links = None
    
    def get_queryset(self, request):
        qs = super(ValidarAsistenteAdmin, self).get_queryset(request)
        ingresados = Asistente_Ingresado.objects.all()
        asistentes = set()
        
        if len(ingresados) > 0:
            for ingresado in ingresados:
                if (ingresado.ingresado == True):
                    asistentes.add(ingresado.asistente.id)
        
        print asistentes
        
        return qs.filter(id__in = asistentes)
    
 
class PuntoControlForm(forms.ModelForm):
    
    class Meta:
        model = PuntoControl
        fields = ('nombre','usuario','evento','actividades',)
        
    def __init__(self, *args, **kwargs):
        super(PuntoControlForm, self).__init__(*args, **kwargs)
        usuario = self.current_user
        
        if usuario.is_superuser:
            self.fields['actividades'].queryset = Actividad.objects.all()
            perfiles = Perfil.objects.filter(rol = 3)
            usuarios = set()
            
            for perfil in perfiles:
                usuarios.add(perfil.usuario.id)
                
            self.fields['usuario'].queryset = User.objects.filter(pk__in = usuarios)
            
        else:
            self.fields['actividades'].queryset = usuario.perfil.evento.actividad_set.all()
            
            perfiles = usuario.perfil.evento.perfil_set.all().filter(rol = 3)
            usuarios = set()
            
            for perfil in perfiles:
                usuarios.add(perfil.usuario.id)
                    
            self.fields['usuario'].queryset = User.objects.filter(pk__in = usuarios)

    
class PuntoControlAdminView(admin.ModelAdmin):
    
    campos_normaluser = ( 
        ("Datos del Punto de control", { 'fields': ('nombre',)}), 
        ("Usuario encargado", { 'fields': ('usuario',)}), 
        ("Actividades Monitoreadas", { 'fields': ('actividades',)}),
    )
    
    campos_superuser = (
        ("Seleccion de Evento", { 'fields': ('evento',)}),               
    )

    list_display = ('id','nombre', 'nombre_usuario','evento','lista_actividades')
    filter_horizontal =  ('actividades',)
    form = PuntoControlForm
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(PuntoControlAdminView, self).get_form(request, obj, **kwargs)
        
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form.current_user = request.user
        return form
    
    def save_model(self, request, obj, form, change):
        
        if request.user.is_superuser:
            obj.save()
            
        else:
            obj.evento = request.user.perfil.evento
            obj.save()
        
    def get_queryset(self, request):
        qs = super(PuntoControlAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__id=request.user.perfil.evento.id)
    
    
    def lista_actividades(self, punto):
        cadena = ''
        actividades = punto.actividades.all()
        
        for actividad in actividades:
            cadena = cadena + actividad.nombre +", "
        
        return cadena
        
    def nombre_usuario(self, punto):
        return punto.usuario.username
    
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1

class PreguntaForm(forms.ModelForm):
    
    class Meta:
        model = Pregunta
        fields = ['actividad','texto']
        
    def __init__(self, *args, **kwargs):
        super(PreguntaForm, self).__init__(*args, **kwargs)
        
        if self.current_user.is_superuser:
            self.fields['actividad'].queryset = Actividad.objects.all()
        else:
            self.fields['actividad'].queryset = self.current_user.perfil.evento.actividad_set.all()
              
class PreguntaAdminView(admin.ModelAdmin):   
    inlines = (OpcionInline,)
    list_display = ('id', 'texto','opciones','actividad','ver_resultados')
    list_filter = (('actividad', admin.RelatedOnlyFieldListFilter),)
    fieldsets = ( 
        ("Datos de la pregunta", { 'fields': ('actividad','texto',)}), 
    )
    ordering = ('id',)
    form = PreguntaForm
    
    def ver_resultados(self, pregunta):
        return format_html("<a href='/admin/Aplicacion/pregunta/grafica/?id_pregunta={0}' target='_self'> <input type='button' id='{0}' value='Resultados' class='default resultados' style='height:22px;width: 90px;padding:1px 1px;'></a>", pregunta.id)
#

    def get_form(self, request, obj = None, **kwargs):
        form = super(PreguntaAdminView, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form
    
    def get_queryset(self, request):
        qs = super(PreguntaAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        actividades = Actividad.objects.filter(evento__id = request.user.perfil.evento.id)
        actividades_ids = []
        
        for actividad in actividades:
            actividades_ids.append(actividad.id)
        
        return qs.filter(actividad_id__in = (actividades_ids))
    
    def opciones(self, pregunta):
        lista_opciones = pregunta.opcion_set.all()
        cadena = ""
        
        for opcion in lista_opciones:
            cadena = cadena + "<li><b>{0})</b> {1}".format(opcion.numeral, opcion.texto)+"</li>"
        
        cadena ="<ul>"+cadena+"</ul>"
        return format_html(cadena)
 
def marcar_duda(modeladmin, request, dudas):
    for duda in dudas:
        if (duda.respondida == True):
            duda.respondida = False
            duda.save()
        else:
            duda.respondida = True
            duda.save()

marcar_duda.short_description = "Marcar / Desmarcar como respondida"   

class DudaAdminView(admin.ModelAdmin):
    list_display = ('id','texto','nombre_usuario', 'respondida')
    list_display_links = None
    actions = [marcar_duda]
    list_filter = (('actividad', admin.RelatedOnlyFieldListFilter),)
    
    def get_queryset(self, request):
        qs = super(DudaAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        actividades = Actividad.objects.filter(evento__id = request.user.perfil.evento.id)
        actividades_ids = []
        
        for actividad in actividades:
            actividades_ids.append(actividad.id)
        
        return qs.filter(actividad_id__in = (actividades_ids))
    
    def nombre_usuario(self, duda):
        return duda.asistente.nombre+' '+ duda.asistente.apellido

class RutaInline(admin.TabularInline):
    model = RutaAudio
    extra = 1   

class ActividadForm(forms.ModelForm):
    
    class Meta:
        model = Actividad
        fields = ('tipo','evento','nombre', 'persona', 'caracter','cupos','informacion', 'imagen','servicios','fecha_inicio','hora_inicio','hora_fin','categorias',)
        
    def __init__(self, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)
        
        if self.current_user.is_superuser:
            print ("super")
            self.fields['servicios'].queryset = Servicio.objects.all()
        else: 
            print ("normal")
            self.fields['servicios'].queryset = self.current_user.perfil.evento.servicios
   
class ActividadAdminView(admin.ModelAdmin):
    
    campos_normaluser = ( 
        ("Datos de la Actividad", { 'fields': ('tipo','nombre', 'persona', 'caracter','cupos')}), 
        ("Descripcion", { 'fields': ('informacion', 'imagen',)}),
        ("Servicios", { 'fields': ('servicios', )}),
        ("Horario", { 'fields': ('fecha_inicio','hora_inicio','hora_fin', )}),
        ("Categorias de asistentes", { 'fields': ('categorias', )}),
    )
    
    campos_superuser = (
        ("Datos del evento", { 'fields': ('evento',)}),
    )

    
    class Media:
        js = ('js/jquery/jquery-1.8.3.js', 'js/owner/actividadAdmin.js')
        
    list_display = ('id','hora_inicio','hora_fin','nombre','tipo','lista_servicios')
    filter_horizontal =  ('categorias','servicios')
    ordering = ('hora_inicio',)
    form = ActividadForm
    list_filter = (('evento', admin.RelatedOnlyFieldListFilter),)
    inlines = (RutaInline,)
    
    def get_form(self, request, obj = None, **kwargs):
        
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form = super(ActividadAdminView, self).get_form(request, obj, **kwargs)
            
        form.current_user = request.user
        return form
    
    def save_model(self, request, obj, form, change):
        
        if not request.user.is_superuser:
            print ("no super usuario")
            obj.evento = request.user.perfil.evento
        obj.save()
        

    def get_queryset(self, request):
        qs = super(ActividadAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__id=request.user.perfil.evento.id)
    
    def lista_servicios(self, actividad):
        cadena = ""
        servicios = actividad.servicios.all()
        
        for servicio in servicios:
            cadena = cadena + "<li>"+servicio.nombre +"</li>"
        
        cadena ="<ul>"+ cadena +"</ul>"
        return format_html(cadena)
    
class AvanceAgenda(Actividad):
        
    class Meta:
        proxy = True
        
class AvanceAgendaAdmin(ActividadAdminView):
    
    class Media:
        js = ('js/owner/miactividadAdmin.js','js/jquery/timepicki.js','js/jquery/jquery.cookie.js',
               'js/jquery/noty/js/noty/packaged/jquery.noty.packaged.min.js',
               'js/jquery/noty/js/noty/layouts/topCenter.js','js/jquery/noty/js/noty/themes/default.js')
        css = {'all': ('css/timepicki.css',)} 
        
    list_display = ('id','ver_hora_inicio','ver_hora_fin','nombre','tipo','guardar_cambios')
    list_display_links = None
    actions = None
    
    def get_queryset(self, request):
        qs = super(AvanceAgendaAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__id = request.user.perfil.evento.id)
    
    def ver_hora_inicio(self, actividad):
        return format_html("<input id='timepickerInicio' class='time_widget' style='width:62px; text-align:center' type='text' name='timepickerInicio' value='{0}'/>", actividad.hora_inicio.strftime('%H:%M'))
    
    def ver_hora_fin(self, actividad):
        return format_html("<input id='timepickerFin' class='time_widget' style='width:62px; text-align:center' type='text' name='timepickerFin' value='{0}'",actividad.hora_fin.strftime('%H:%M'))
    
    def guardar_cambios(self, actividad):
        return format_html("<input type='button' id='{0}' value='Guardar' class='default guardar' style='height:22px;width: 90px;padding:1px 1px;'>", actividad.id)

class InformacionForm(forms.ModelForm):
    
    class Meta:
        model = Informacion
        fields = ('fecha_inicio','fecha_fin','evento', 'logo','localizacion','patrocinadores',)        

class InformacionAdminView (admin.ModelAdmin):
    campos_normaluser = ( 
        ("Informacion del Evento", { 'fields': ('fecha_inicio','fecha_fin', 'logo',)}),
        ("Localizacion", { 'fields': ('localizacion',)}) ,
        ("Patrocinadores", { 'fields': ('patrocinadores',)})
        )
    
    campos_superuser = (
        ("Evento", { 'fields': ('evento',)}),
        )
    
    list_display = ('evento','fecha_inicio','fecha_fin')
    filter_horizontal = ('patrocinadores',)
        
    def save_model(self, request, obj, form, change):
        
        if request.user.is_superuser:
            obj.save()
            
        else:
            informacion = Informacion.objects.filter(evento__id = request.user.perfil.evento.id)
            
            if (len(informacion) >0):
                obj.id = informacion[0].id
                obj.evento = request.user.perfil.evento
                obj.save()
            else:
                obj.evento = request.user.perfil.evento
            obj.save()
            
    def get_form(self, request, obj = None, **kwargs):
        form = super(InformacionAdminView, self).get_form(request, obj, **kwargs)
                
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form.current_user = request.user
        return form
            
    def get_queryset(self, request):
        qs = super(InformacionAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__id=request.user.perfil.evento.id)

class PatrocinadorAdminView (admin.ModelAdmin):
    fieldsets = ( 
        ("Datos del Patrocinador", { 'fields': ('nombre','hipervinculo',)}),
        ("Imagenes", { 'fields': ('logo','baner',)}),
        )
    list_display = ('id','nombre','hipervinculo')
  
class MemoriaForm(forms.ModelForm):
    
    class Meta:
        model = Memoria
        fields = ('actividad','nombre','descripcion','archivo')     
           
    def __init__(self, *args, **kwargs):
        super(MemoriaForm, self).__init__(*args, **kwargs)
        
        if self.current_user.is_superuser:
            self.fields['actividad'].queryset = Actividad.objects.all()
        else:
            self.fields['actividad'].queryset = self.current_user.perfil.evento.actividad_set.all()
        
          
class MemoriaAdminView(admin.ModelAdmin):
    fieldsets = ( 
        ("Datos de la Memoria", { 'fields': ('actividad','nombre','descripcion',)}),
        ("Subir archivo", { 'fields': ('archivo',)}),
        )
    list_display = ('id','nombre','descripcion','actividad')
    form = MemoriaForm
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(MemoriaAdminView, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form
    
    def get_queryset(self, request):
        qs = super(MemoriaAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        actividades = Actividad.objects.filter(evento__id = request.user.perfil.evento.id)
        actividades_ids = []
        
        for actividad in actividades:
            actividades_ids.append(actividad.id)
        
        return qs.filter(actividad_id__in = (actividades_ids))
    
class EmpresaAdminView(admin.ModelAdmin):
    campos_normaluser = ( 
        ("Datos de la Empresa", { 'fields': ('nombre','logo','descripcion',)}),
        )
    
    campos_superuser = (
        ("Evento", { 'fields': ('evento',)}),
        )
    
    list_display = ('id','nombre','descripcion')
    
    def save_model(self, request, obj, form, change):
        
        if not request.user.is_superuser:
            obj.evento = request.user.perfil.evento
        obj.save()
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(EmpresaAdminView, self).get_form(request, obj, **kwargs)
                
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form.current_user = request.user
        return form
    
    def get_queryset(self, request):
        qs = super(EmpresaAdminView, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        else:
            return qs.filter(evento__id = request.user.perfil.evento.id)
    
class MuestraComercialForm(forms.ModelForm):
    
    class Meta:
        model = MuestraComercial
        fields = ('nombre_empresa','stand','evento','logo','email','hipervinculo',)     
           
class MuestraComercialAdmin(admin.ModelAdmin):
    
    campos_normaluser = ( 
        ("Datos Principales", { 'fields': ('nombre_empresa','stand','logo')}),
        ("Datos de contacto", { 'fields': ('email','hipervinculo',)}),
        )
    
    campos_superuser = (
        ("Seleccion de Evento", { 'fields': ('evento',)}),
    )
    list_display = ('id','nombre_empresa','hipervinculo','email')
    
    def save_model(self, request, obj, form, change):
        
        if request.user.is_superuser:
            obj.save()
            
        else:
            obj.evento = request.user.perfil.evento
            obj.save()
        
    def get_form(self, request, obj = None, **kwargs):
        form = super(MuestraComercialAdmin, self).get_form(request, obj, **kwargs)
                
        if request.user.is_superuser:
            self.fieldsets = self.campos_superuser + self.campos_normaluser
            
        else:
            self.fieldsets = self.campos_normaluser
            
        form.current_user = request.user
        return form
    
    def get_queryset(self, request):
        qs = super(MuestraComercialAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__id=request.user.perfil.evento.id)

class CategoriaAdminView(admin.ModelAdmin):
    fieldsets = ( 
        ("Datos Principales", { 'fields': ('nombre','descripcion')}),
        )
    list_display = ('id','nombre','descripcion');
    

admin.site.unregister(User)
admin.site.register(User,UsuarioAdmin)
admin.site.register(Evento, EventoAdminView)
admin.site.register(Servicio, ServicioAdminView)
admin.site.register(Actividad, ActividadAdminView)
admin.site.register(AvanceAgenda, AvanceAgendaAdmin)
admin.site.register(Categoria, CategoriaAdminView)
admin.site.register(Empresa, EmpresaAdminView)
admin.site.register(Patrocinador, PatrocinadorAdminView)
admin.site.register(Memoria, MemoriaAdminView)
admin.site.register(MuestraComercial, MuestraComercialAdmin)
admin.site.register(Asistente, AsistenteAdminView)
admin.site.register(ValidarAsistente, ValidarAsistenteAdmin)
admin.site.register(PuntoControl, PuntoControlAdminView)
admin.site.register(Pregunta, PreguntaAdminView)
admin.site.register(Duda, DudaAdminView)
admin.site.register(Informacion,InformacionAdminView)


# Register your models here.
