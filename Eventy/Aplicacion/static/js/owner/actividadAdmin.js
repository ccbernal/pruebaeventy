$(document).ready(function()
{

	$("div.field-cupos").hide();


	$("#id_caracter").on('change', function() 
	{
		if (this.value == "Abierta")
		{
			$("div.field-cupos").hide();
			$("#id_cupos").val(0);
		}
		if (this.value == "Cerrada")
		{
			$("div.field-cupos").show();
		}
	});

	
	

	
});