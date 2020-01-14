//window.onbeforeunload = function(){
//    if (typeof editandoproyecto === 'undefined')// en la template de modificar_projecte se crea la variable,asi que si no existe es que no se esta modificando el proyecto
//        load = loading("Carregant..."); //al final parece que esto no causa problemas de rendimiento
//    else
//        return 'Segur que vols sortir?';
//
//
//};

$(window).on('unload', function() {

});

$(document).ready(function(){
//    mostrar_menu("#contenedor_general");
//    $("#general").parent("li").addClass("active");
//
//    $("#general").click(function(){
//        mostrar_menu("#contenedor_general");
//        $(this).parent("li").addClass("active");
//    });
//
//    $("#personal").click(function(){
//        mostrar_menu("#contenedor_personal");
//        $(this).parent("li").addClass("active");
//    });
//
//    $("#finançament").click(function(){
//        mostrar_menu("#contenedor_finançament");
//        $(this).parent("li").addClass("active");
//    });
//
//    $("#pressupost").click(function(){
//        mostrar_menu("#contenedor_pressupost");
//        $(this).parent("li").addClass("active");
//    });
//
//    $("#justificacions").click(function(){
//        mostrar_menu("#contenedor_justificacions");
//        $(this).parent("li").addClass("active");
//    });
//
//    if($('#contenedor_iconos').length){
//        $(".titulo").fadeIn(700);
//
//        setTimeout( function(){
//            $(".opcion:hidden:first").slideDown(200);
//        },600 );
//        setTimeout( function(){
//            $(".opcion:hidden:first").slideDown(200);
//        },700 );
//        setTimeout( function(){
//            $(".opcion:hidden:first").slideDown(200);
//        },800 );
//        setTimeout( function(){
//            $(".opcion:hidden:first").slideDown(200);
//        },900 );
//    }

//    $('.btn-confirmacion').click(function(e){
//		e.preventDefault();
//		$('#confirmacion').modal('show');
//	});

//esto se ejecutara solo una vez al cargar
;
$("#contenedor_personal").hide();
$("#contenedor_finançament").hide();
$("#contenedor_pressupost").hide();
$("#contenedor_justificacions").hide();
$("#contenedor_compromes").hide();
$("#general").addClass("active");

$("#general").click(function(){
    mostrar_menu("#contenedor_general");
    $(this).addClass("active");
});

$("#personal").click(function(){
    mostrar_menu("#contenedor_personal");
    $(this).addClass("active");
});

$("#finançament").click(function(){
    mostrar_menu("#contenedor_finançament");
    $(this).addClass("active");
});

$("#pressupost").click(function(){
    mostrar_menu("#contenedor_pressupost");
    $(this).addClass("active");
});

$("#justificacions").click(function(){
    mostrar_menu("#contenedor_justificacions");
    $(this).addClass("active");
});

$("#compromes").click(function(){
    mostrar_menu("#contenedor_compromes");
    $(this).addClass("active");
});

////////DIALOGS
	$("#dialogs").dialog({
        resizable:true,
        modal:true,
        width:"1000px",
        autoOpen:false,
        show: {
            effect: "fade",
            duration: 500
        },
        hide: {
            effect: "fade",
            duration: 500
        }
	});


	$("#dialogs").dialog("close");

	$("#mostrar_participants_organismes").click(function(){
	    mostrar_dialog("table_participants_organismes");
	});


    $("#mostrar_usuaris_externs").click(function(){
	    mostrar_dialog("table_usuaris_externs");
	});

    $("#mostrar_usuaris_creaf").click(function(){
	    mostrar_dialog("table_usuaris_creaf");
	});

	$("#mostrar_editar_justificacio_personal").click(function(){
	    $("#formulario_editar_justificacio_personal").trigger("reset");
	    $("#formulario_editar_justificacio_personal").children("[name='id_perso_creaf']").val(id_current_perso_creaf);
	    $("#formulario_editar_justificacio_personal").attr("action","/gestor_JustificPersonal/");
	    $("#formulario_editar_justificacio_personal").attr("method","POST");
	    mostrar_dialog("editar_justificacio_personal");
    });
    ///mostrar dialog justificacions personal esta en funciones_datatables



//    $("#mostrar_editar_organismes_participants_editar").click(function(){
//	    mostrar_dialog("editar_organismes_participants");
//	    $("#editar_organismes_participants").attr("method","PUT")
//	});


	 $("#boton_guardar").click(function(e){
	    $.confirm({
            title: 'Guardar projecte',
            content: "Segur que vols guardar?",
            confirmButton: 'Si',
            cancelButton: 'Cancel·lar',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            confirm: function(){
                loading("Guardant canvis...");
                $("#formulario_nou_projecte").submit();
            }
        });
	 });


    $("#select_id_responsable").change(function(e){
        $("#id_id_resp").val($("#select_id_responsable").val());
    })

    $("#select_id_usuari_extern").change(function(e){
        $("#id_id_usuari_extern").val($("#select_id_usuari_extern").val());
    })

    ///ACTUALIZAR SELECTS *OJO LOS OTROS 2 ACTUALIZAR ESTAN EN FUNCIONES CABECERA
    if(Admin==1){
        if($("#formulario_nou_projecte").length){
            actualizar_conceptes_press_select();
            actualizar_organismes_select();
            actualizar_usuaris_externs_select();
        }
    }
});

/////ACTUALIZAR LOS SELECTS

function actualizar_organismes_select(){
        $(".select_id_organisme").each(function(){
            $(this).html("<option>CARREGANT...</option>");
        });
        $.ajax({
                    url: '/llista_organismes_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.nom+"</option>";
                        });
                        $(".select_id_organisme").each(function(){
                            if($(this).attr("id")=="filtre_financadors"){//Este es solo para el select de la pagina principal de comptabilitat
                                $(this).html("<option value='default' selected='selected'>*Opcional*--ORGANISME FINANÇADOR--</option>"+html);
                                //$("#filtre_financadors").prepend($("<option value='default' selected='selected'>--ESCOLLIR ORGANISME FINANÇADOR--</option>"));
                            }else{
                                $(this).html(html);
                            }

                        });
                        //$("#select_id_organisme").html(html);

                    }

        });
}

function actualizar_conceptes_press_select(){
        $.ajax({
                    url: '/llista_ConceptesPres/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.descripcio+"</option>";
                        });
                        $("#select_id_concepte_pres").html(html);

                    }

        });
}

function actualizar_usuaris_creaf_select(){
        $.ajax({
                    url: '/llista_usuaris_creaf_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.nom+"</option>";
                        });
                        $(".select_id_usuari_creaf").each(function(){
                            $(this).html(html);
                        });
                        //$("#select_id_organisme").html(html);

                    }

        });
}

function actualizar_usuaris_xarxa_select(){
        $.ajax({
                    url: '/llista_usuaris_xarxa_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.nom+"</option>";
                        });
                        $(".select_id_usuari_xarxa").each(function(){
                            $(this).html(html);
                        });
                        //$("#select_id_organisme").html(html);

                    }

        });
}

function actualizar_usuaris_externs_select(){
        $.ajax({
                    url: '/llista_usuaris_externs_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="<option value=''>--------</option>";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.nom+" --- "+this.organisme+"</option>";
                        });

                        $("#select_id_usuari_extern").html(html);
                        //seleccionamos la opcion que se carga
                        $('#select_id_usuari_extern option[value="'+$("#id_id_usuari_extern").val()+'"]').attr('selected', 'selected');

                        //$("#select_id_organisme").html(html);
                    }

        });
}

function actualizar_responsables_select(){
        $.ajax({
                    url: '/llista_responsables_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="<option value=''>--------</option>";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.codi+" - "+this.nom+"</option>";
                        });

                        $(".select_id_responsable").each(function(){
                            $(this).html(html);
                        });

                        $("#select_id_responsable").html(html);
                        //seleccionamos la opcion que se carga
                        $('#select_id_responsable option[value="'+$("#id_id_resp").val()+'"]').attr('selected', 'selected');

                        //$("#select_id_organisme").html(html);
                    }

        });
}
function actualizar_projectes_select(){
        $.ajax({
                    url: '/llista_projectes_select/',
//                    type: form.attr('method'),
//                    data: form.serialize(),
                    datatype:'json',
                    success: function(result) {
                        var html="";
                        $(result).each(function(){
                            html=html+"<option value='"+this.id+"'>"+this.acronim+"</option>";
                        });
                        $(".select_id_projecte").each(function(){
                            $(this).html(html);
                        });
                        //$("#select_id_organisme").html(html);

                    }

        });
}


///////////////

function mostrar_menu(nombre){
var id_div;
$("#formulario_nou_projecte").children("div").each(function(){
    if(!$(this).is(':hidden'))
        id_div=$(this).attr('id');
});

$("#"+id_div).hide("drop",{direction:"left",complete(){
    $(nombre).show("drop",{direction:"right",complete(){
        $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();///IMPORTANTE sirve para alinear correctamente las cabeceras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
    }},300);
}},300);

//los botones los ponemos del color original
$("#general").removeClass("active");
$("#personal").removeClass("active");
$("#finançament").removeClass("active");
$("#pressupost").removeClass("active");
$("#justificacions").removeClass("active");
$("#compromes").removeClass("active");
}


//crear un script aparte con para mentener mas orden,ya que esta funcion tambien lo usa resum fitxa major comptes en contabilidad
function mostrar_dialog(dialog){
//    var titulo = "";
    $("#dialogs").dialog("open");
    $(".dialogcont").each(function(){
        $(this).hide();
        if($(this).attr("id")==dialog){
             $(this).show();
    //         titulo = $(this).attr("title");
             $("#dialogs").dialog({"title":$(this).attr("title")});
        }
    });
    $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
//   var dia= $.dialog({
//        title:titulo,
//        content:"",
//        confirmButton: false,
//        closeIcon: true,
//        backgroundDismiss: true,
//        columnClass: 'col-md-6 col-md-offset-3'
//    });
//    dia.setContent($("#dialogs"));
}