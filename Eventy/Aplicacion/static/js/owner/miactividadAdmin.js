$(document).ready(function()
{

	var times = $('input.time_widget');

	for (var i = 0; i < times.length; i++) 
	{
		var hora = $(times[i]).val().split(':'); 
		$(times[i]).timepicki({show_meridian:false,min_hour_value:0,max_hour_value:23,start_time: [hora[0], hora[1]]});
	};

	$(".guardar").on("click",function(){
		var hora_inicio = $(this).parent().parent().children("td.field-ver_hora_inicio").children("div.time_pick").children("input.time_widget").val();
		var hora_fin = $(this).parent().parent().children("td.field-ver_hora_fin").children("div.time_pick").children("input.time_widget").val();
		var actividad_id = this.id; 

		$.ajax
		({
			   url: 'http://localhost:8000/cambiar_hora/',
			   data:{'actividad_id' : actividad_id, 'hora_inicio':hora_inicio , 'hora_fin':hora_fin },
			   dataType: 'json',
			   type: 'POST',
			   headers : {'X-CSRFToken': $.cookie('csrftoken')},
		})
		.done(function(mensaje){
			notificar('success',mensaje.mensaje);
		});
		window.setTimeout('location.reload()',3);
	});

	function notificar(tipo,mensaje)
	{
		noty({
					text: mensaje,
					type: tipo,
					layout:'topCenter', 
					theme:'defaultTheme',
					animation: {
					    open: {height: 'toggle'}, // or Animate.css class names like: 'animated bounceInLeft'
					    close: {height: 'toggle'}, // or Animate.css class names like: 'animated bounceOutLeft'
					    easing: 'swing',
					    speed: 500 // opening & closing animation speed
  					},
  					closeWith: ['click','hover'],
				});
	}

});