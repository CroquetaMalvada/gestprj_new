var load = null;
$(document).ready(function(){
	$("#loading").dialog({
        modal:true,
        resizable:false,
        draggable:false,
        closeOnEscape:false,
        autoOpen:false,
        dialogClass: "noclose"
	});

    $(document).on({

        ajaxStart: function(){
            if($(this).find(".dataTables_empty")){
                var mensaje=$(this).find(".dataTables_empty");
                mensaje.html("Carregant...");
            }
            load = loading("Carregant...");
        },
        ajaxStop: function(){
            if($(this).find(".dataTables_empty")){
                var mensaje=$(this).find(".dataTables_empty");
                mensaje.html("No s'han trobat dades");
            }
        load.close();
        }
    });

});

function loading(texto){
        return $.alert({//este alert se usa del jquery-confirm y sirve para que se carge antes que el ajax
            title:texto,
            content:'<img src="'+$("#loading").attr("src")+'"/>',
            confirmButton: false
        });

//        if(cerrable==true)
//            return load;
}

function alerterror(){
    $("#diverror").dialog({
        modal:true,
        resizable:false,
        draggable:false,
        closeOnEscape:true,
        autoOpen:true,
        content:$("#diverror"),
        confirmButton: "OK"
	});

}

function alertsuccess(texto){
    var load = $.alert({
            title:texto,
            content:'<img src="'+$("#alertsuccess").attr("src")+'"/>',
            confirmButton: "OK"
    });
}