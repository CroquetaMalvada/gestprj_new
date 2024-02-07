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
//        ajaxStart: function(){$("#loading").dialog("open");},
//        ajaxStop: function(){$("#loading").dialog("close");}
        ajaxStart: function(){load = loading("Carregant...",true);},
        ajaxStop: function(){load.close();}
    });

});

function loading(texto,cerrable){
        var load = $.alert({
            title:texto,
            content:'<img src="http://bestanimations.com/Science/Gears/loadinggears/loading-gears-animation-10.gif"/>',
            confirmButton: false
        });

        if(cerrable==true)
            return load;
}