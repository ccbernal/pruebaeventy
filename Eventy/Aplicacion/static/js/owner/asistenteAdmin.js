$(document).ready(function()
{
	
	if ($("#id_evento").length)
	{
		iniciarActividades($("#id_evento").val());
	}

	function iniciarActividades(evento_id)
	{
		
		if(evento_id == '')
		{
			$("#id_actividades option").remove();
		}
		else
		{
			$("#id_actividades option").remove();
			obtenerActividades(evento_id);
		}
	}


	$("#id_evento").on('change', function()
			{
				iniciarActividades(this.value);
			}
	);

	function obtenerActividades(evento_id) 
	{
		console.log(evento_id);
		$.ajax
		({
			   url: 'http://localhost:8000/obtener_actividades/',
			   data:{'id_evento' : evento_id, },
			   dataType: 'json',
			   type: 'POST',
			   headers : {'authorization': 'Token 0000'}
		})
		.done(function(actividades){
			$.each(actividades, function (i, actividad) 
			{
	    		$('#id_actividades').append($('<option>', { 
	        		value: actividad.id,
	        		text : actividad.nombre,
	    		}));
			});
		});
	}

	
});