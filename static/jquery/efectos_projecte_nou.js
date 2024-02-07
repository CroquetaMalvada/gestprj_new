$(document).ready(function(){
    mostrar_menu("#contenedor_general");
    $("#general").parent("li").addClass("active");

    $("#general").click(function(){
        mostrar_menu("#contenedor_general");
        $(this).parent("li").addClass("active");
    });

    $("#personal").click(function(){
        mostrar_menu("#contenedor_personal");
        $(this).parent("li").addClass("active");
    });

    $("#finançament").click(function(){
        mostrar_menu("#contenedor_finançament");
        $(this).parent("li").addClass("active");
    });

    $("#pressupost").click(function(){
        mostrar_menu("#contenedor_pressupost");
        $(this).parent("li").addClass("active");
    });

    $("#justificacions").click(function(){
        mostrar_menu("#contenedor_justificacions");
        $(this).parent("li").addClass("active");
    });

    if($('#contenedor_iconos').length){
        $(".titulo").fadeIn(700);

        setTimeout( function(){
            $(".opcion:hidden:first").slideDown(200);
        },600 );
        setTimeout( function(){
            $(".opcion:hidden:first").slideDown(200);
        },700 );
        setTimeout( function(){
            $(".opcion:hidden:first").slideDown(200);
        },800 );
        setTimeout( function(){
            $(".opcion:hidden:first").slideDown(200);
        },900 );
    }

//    $('.btn-confirmacion').click(function(e){
//		e.preventDefault();
//		$('#confirmacion').modal('show');
//	});


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

	$("#mostrar_editar_organismes_participants_crear").click(function(){
	    $("#formulario_editar_organismes_participants").trigger("reset");
	    $("#formulario_editar_organismes_participants").attr("action","/gestor_TOrganismes/");
	    $("#formulario_editar_organismes_participants").attr("method","POST");
	    mostrar_dialog("editar_organismes_participants");
//	    $("#editar_organismes_participants").cattr("method","POST")
	});

	$("#mostrar_editar_personal_creaf_crear").click(function(){
	    $("#formulario_editar_usuari_creaf").trigger("reset");
	    $("#formulario_editar_usuari_creaf").attr("action","/gestor_UsuariCreaf/");
	    $("#formulario_editar_usuari_creaf").attr("method","POST");
	    mostrar_dialog("editar_usuari_creaf");
//	    $("#editar_organismes_participants").attr("method","POST")
	});


	$("#mostrar_editar_personal_extern_crear").click(function(){
	    $("#formulario_editar_usuari_extern").trigger("reset");
	    $("#formulario_editar_usuari_extern").attr("action","/gestor_UsuariExtern/");
	    $("#formulario_editar_usuari_extern").attr("method","POST");
	    mostrar_dialog("editar_usuari_extern");
//	    $("#editar_organismes_participants").attr("method","POST")
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

});



function mostrar_menu(nombre){
$("#contenedor_general").hide();
$("#contenedor_personal").hide();
$("#contenedor_finançament").hide();
$("#contenedor_pressupost").hide();
$("#contenedor_justificacions").hide();

$("#general").parent("li").removeClass("active");
$("#personal").parent("li").removeClass("active");
$("#finançament").parent("li").removeClass("active");
$("#pressupost").parent("li").removeClass("active");
$("#justificacions").parent("li").removeClass("active");

$(nombre).show();

$.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();///IMPORTANTE sire para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
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