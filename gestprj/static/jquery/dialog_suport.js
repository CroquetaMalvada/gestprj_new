$(document).ready(function(){
	 $("#boton_suport").click(function(e){
	    $.confirm({
            title: 'Suport',
            content: "Clica en el següent enllaç per informar de la teva incidencia o proposta per correu:<br><a href='mailto:gestprj.suport@creaf.uab.cat'><input type='button' value='Contactar' /></a>",
            confirmButton: false,
            cancelButton: 'Tancar',
            cancelButtonClass: 'btn-info'
        });
	 });
 });