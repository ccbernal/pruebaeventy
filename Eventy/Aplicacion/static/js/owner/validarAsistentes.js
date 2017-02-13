$(document).ready(function(){

	$('#buscar').on("click",function(){

		var celular = $('#celular').val();
		var id_actividad = $('#actividad').val();

		if(id_actividad != 0)
		{
			$.ajax
			({
				   url: 'http://localhost:8000/validar_asistente/',
				   data:{'id_actividad': id_actividad, 'celular':celular},
				   dataType: 'json',
				   type: 'POST',
				   headers : {'X-CSRFToken': $.cookie('csrftoken')},
			})
			.done(function(mensaje){
				
				if (mensaje.mensaje == 1)
				{
					notificar('success','Se ha ingresado correctamente el asistente');
					actualizarTabla(id_actividad);
				}
				else if (mensaje.mensaje == 2)
				{
					notificar('warning','El asistente ya habia ingresado a esta actividad');
				}
				else
				{
					notificar('error','No se encontrado un asistente con el numero de celular '+celular);
				}
				
			});
		}
		else
		{
			notificar('warning','Debe seleccionar una actividad');
		}
	});

	$('#actividad').on('change',function(){

		if($(this).val() != 0)
		{

			actualizarTabla($(this).val());
		}
		else
		{
			$('#result_list tbody').remove();
		}

	});

	function actualizarTabla(id_actividad)
	{
			$.ajax
			({
				   url: 'http://localhost:8000/obtener_asistentes/',
				   data:{'id_actividad': id_actividad},
				   dataType: 'json',
				   type: 'POST',
				   headers : {'X-CSRFToken': $.cookie('csrftoken')},
			})
			.done(function(asistentes){
				var cadena = "<tbody>";
				$.each(asistentes,function(i, item){
					cadena = cadena + "<tr class='row1'>"+
											"<th class='field-id'>"+item.id+"</th>"+
											"<td class='field-nombre'>"+item.nombre+"</td>"+
											"<td class='field-apellido'>"+item.apellido+"</td>"+
											"<td class='field-celular'>"+item.celular+"</td>"+
											"<td class='field-email'>"+item.email+"</td>"+
											"<td class='field-empresa nowrap'>Empresa</td>"+
											"<td class='field-cargo'>"+item.cargo+"</td>"+
											"<td class='field-activo'><img src='/static/admin/img/icon-yes.svg' alt='True'></td>"+
										"</tr>";
				});
				cadena = cadena +"</tbody>";
				$('#result_list tbody').remove();
				$('#result_list').append(cadena);
			});

	}

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