$(document).ready(function(){
    ////////// DATATABLES DE LA OPCION "EDICIO" !!!!!!!!

    //////////ORGANISMES
    var organismes_cabecera= $("#table_organismes_cabecera").children("table").DataTable({
            ajax: {
                url: '/llista_Organismes/',
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_organisme'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-info editar_organisme_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_organisme_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]}
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
    });
    /////////////USUARIS CREAF
    var usuaris_creaf_cabecera = $("#table_usuaris_creaf_cabecera").children("table").DataTable({
            ajax: {
                url: '/llista_Usuaris_creaf/',
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_usuari'},
                {'data': 'nom_usuari'},
                {"render": function(){return '<a class="btn btn-info editar_usuari_creaf_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_usuari_creaf_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]},
                { "width": "5%", "targets": [3,4] }
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });
    /////////////USUARIS EXTERNS
    var usuaris_externs_cabecera = $("#table_usuaris_externs_cabecera").children("table").DataTable({
            ajax: {
                url: '/llista_Usuaris_externs/',
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_usuari_extern'},
                {'data': 'nom_usuari_extern'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-info editar_usuari_extern_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_usuari_extern_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]}
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });


    ///////////////////////////////////////////////////////


//    $(document).on('click','.afegir_a_centres_participants_cabecera',function(){
//    //        if($.inArray(organismes.row('.selected').data()["nom_organisme"],centres_participants.column(1).data()) != -1){//si ya está ese organismo en los participantes
//    //            alert("Aquest organisme ja està participant en aquest projecte.");
//    //        }else{
//                 $.ajax({
//                    url: "/gestor_centresPart/",
//                    type: "POST",
//                    data: {
//                        "id_projecte":id_prj,
//                        "id_organisme":organismes.row('.selected').data()["id_organisme"]
//                    },
//                    success: function(result) {
//    //                     $("#dialogs").dialog("close");
//                            organismes.$('tr.selected').hide("highlight",{color:"green"},function(){
//                         });
//
//                    }
//                 });
//    //         }
//    });


//
//	$("#mostrar_participants_organismes").click(function(){
//	    mostrar_dialog("table_participants_organismes");
//	});
//
//
//    $("#mostrar_usuaris_externs").click(function(){
//	    mostrar_dialog("table_usuaris_externs");
//	});
//
//    $("#mostrar_usuaris_creaf").click(function(){
//	    mostrar_dialog("table_usuaris_creaf");
//	});


    ////// ORGANISMES
    $(document).on( 'click', '.editar_organisme_cabecera', function (){

        var form = $("#formulario_editar_organismes_cabecera");
        $("#formulario_editar_organismes_cabecera").attr("action",organismes_cabecera.row(".selected").data()["url"]);
	    $("#formulario_editar_organismes_cabecera").attr("method","PUT");
        $.get(organismes_cabecera.row(".selected").data()["url"],function( data ){
            form.children("[name='nom_organisme']").val(data["nom_organisme"]);
            form.children("[name='contacte']").val(data["contacte"]);
            form.children("[name='adreca']").val(data["adreca"]);
            form.children("[name='cp']").val(data["cp"]);
            form.children("[name='poblacio']").val(data["poblacio"]);
            form.children("[name='provincia']").val(data["provincia"]);
            form.children("[name='pais']").val(data["pais"]);
            form.children("[name='tel1']").val(data["tel1"]);
            form.children("[name='tel2']").val(data["tel2"]);
            form.children("[name='fax']").val(data["fax"]);
            form.children("[name='e_mail1']").val(data["e_mail1"]);
            form.children("[name='e_mail2']").val(data["e_mail2"]);
        }).done(function( data ){});

        actualizar_organismes();
        mostrar_dialog_cabecera("editar_organismes_cabecera");

    });

    $(document).on( 'click', '.eliminar_organisme_cabecera', function (){
         $.confirm({
            title: 'Confirmació',
            content: "Segur que vols eliminar aquest element?",
            confirmButton: 'Si',
            cancelButton: 'No',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            closeIcon: false,
            confirm: function(){
                $.ajax({
                    type: "DELETE",
                    url: organismes_cabecera.row(".selected").data()["url"],
                    success: function(result) {
                         organismes_cabecera.$('tr.selected').hide("highlight",{color:"green"},function(){
                            organismes_cabecera.ajax.reload();
                            actualizar_organismes();
                         });
                    }
                });
            },
            cancel: function(){
            }
        });

    });

    ///CREAR UNO
    	$("#editar_organismes_crear_cabecera").click(function(){
	    $("#formulario_editar_organismes_cabecera").trigger("reset");
	    $("#formulario_editar_organismes_cabecera").attr("action","/gestor_TOrganismes/");
	    $("#formulario_editar_organismes_cabecera").attr("method","POST");
	    mostrar_dialog_cabecera("editar_organismes_cabecera");
	});

   /// AJAX
    $("#formulario_editar_organismes_cabecera").submit(function(e){
        var form = $(this);
        if(validar_form(form)){
            $.ajax({
                        url: form.attr('action'),
                        type: form.attr('method'),
    //                    headers: { 'X-HTTP-Method-Override':  }, //no todos los navegadores aceptan DELETE o PUT,con esto se soluciona
                        data: form.serialize(),
                        success: function(result) {
                             mostrar_dialog_cabecera("table_organismes_cabecera");
                             organismes_cabecera.ajax.reload();
                             actualizar_organismes();
                        }

            });
        }
        e.preventDefault(); //para no ejecutar el actual submit del form
    });


    /////////////////////////////////////////////

    ////// USUARIS CREAF

    $(document).on( 'click', '.editar_usuari_creaf_cabecera', function (){

        var form = $("#formulario_editar_usuari_creaf_cabecera");
        $("#formulario_editar_usuari_creaf_cabecera").attr("action",usuaris_creaf_cabecera.row(".selected").data()["url"]);
	    $("#formulario_editar_usuari_creaf_cabecera").attr("method","PUT");

        $.get(usuaris_creaf_cabecera.row(".selected").data()["url"],function( data ){
            form.children("[name='nom_usuari']").val(data["nom_usuari"]);
            form.children("[name='adreca']").val(data["adreca"]);
            form.children("[name='cp']").val(data["cp"]);
            form.children("[name='poblacio']").val(data["poblacio"]);
            form.children("[name='provincia']").val(data["provincia"]);
            form.children("[name='pais']").val(data["pais"]);
            form.children("[name='tel1']").val(data["tel1"]);
            form.children("[name='tel2']").val(data["tel2"]);
            form.children("[name='fax']").val(data["fax"]);
            form.children("[name='e_mail1']").val(data["e_mail1"]);
            form.children("[name='e_mail2']").val(data["e_mail2"]);
            form.children("[name='id_organisme']").val(data["id_organisme"]);
        }).done(function( data ){});

        usuaris_creaf_cabecera.ajax.reload();
        mostrar_dialog_cabecera("editar_usuari_creaf_cabecera");
    });

    $(document).on( 'click', '.eliminar_usuari_creaf_cabecera', function (){

      $.confirm({
            title: 'Confirmació',
            content: "Segur que vols eliminar aquest element?",
            confirmButton: 'Si',
            cancelButton: 'No',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            closeIcon: false,
            confirm: function(){
            $.ajax({
                url: usuaris_creaf_cabecera.row(".selected").data()["url"],
                type: "DELETE",
                success: function(result) {
                     usuaris_creaf_cabecera.ajax.reload();
                }
             });
            },
            cancel: function(){
            }
        });
    });

    //// CREAR UNO
	$("#editar_personal_creaf_crear_cabecera").click(function(){
	    $("#formulario_editar_usuari_creaf_cabecera").trigger("reset");
	    $("#formulario_editar_usuari_creaf_cabecera").attr("action","/gestor_UsuariCreaf/");
	    $("#formulario_editar_usuari_creaf_cabecera").attr("method","POST");
	    mostrar_dialog_cabecera("editar_usuari_creaf_cabecera");
//	    $("#editar_organismes_participants").attr("method","POST")
	});

    /// AJAX
    $("#formulario_editar_usuari_creaf_cabecera").submit(function(e){
        var form = $(this);
        if(validar_form(form)){
            $.ajax({
                        url: form.attr('action'),
                        type: form.attr('method'),
                        data: form.serialize(),
                        success: function(result) {
                             mostrar_dialog_cabecera("table_usuaris_creaf_cabecera");
                             usuaris_creaf_cabecera.ajax.reload();
                        }
            });
        }
        e.preventDefault(); //para no ejecutar el actual submit del form
    });


    ///////////////////////////////////////////////////
    ///////// USUARIS EXTERNS

    $(document).on( 'click', '.editar_usuari_extern_cabecera', function (){
//        var load = loading("Carregant...");
        var form = $("#formulario_editar_usuari_extern_cabecera");
        $("#formulario_editar_usuari_extern_cabecera").attr("action",usuaris_externs_cabecera.row(".selected").data()["url"]);
	    $("#formulario_editar_usuari_extern_cabecera").attr("method","PUT");

        $.get(usuaris_externs_cabecera.row(".selected").data()["url"],function( data ){
            form.children("[name='nom_usuari_extern']").val(data["nom_usuari_extern"]);
            form.children("[name='adreca']").val(data["adreca"]);
            form.children("[name='cp']").val(data["cp"]);
            form.children("[name='poblacio']").val(data["poblacio"]);
            form.children("[name='provincia']").val(data["provincia"]);
            form.children("[name='pais']").val(data["pais"]);
            form.children("[name='tel1']").val(data["tel1"]);
            form.children("[name='tel2']").val(data["tel2"]);
            form.children("[name='fax']").val(data["fax"]);
            form.children("[name='e_mail1']").val(data["e_mail1"]);
            form.children("[name='e_mail2']").val(data["e_mail2"]);
            form.children("[name='id_organisme']").val(data["id_organisme"]);
        }).done(function( data ){});
        usuaris_externs_cabecera.ajax.reload();
        mostrar_dialog_cabecera("editar_usuari_extern_cabecera");

    });

     $(document).on( 'click', '.eliminar_usuari_extern_cabecera', function (){

        $.confirm({
            title: 'Confirmació',
            content: "Segur que vols eliminar aquest element?",
            confirmButton: 'Si',
            cancelButton: 'No',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            closeIcon: false,
            confirm: function(){
            $.ajax({
                url: usuaris_externs_cabecera.row(".selected").data()["url"],
                type: "DELETE",
                success: function(result) {
                     usuaris_externs_cabecera.ajax.reload();
                }
             });
            },
            cancel: function(){
            }
        });
    });

        //// CREAR UNO
        $("#editar_personal_extern_crear_cabecera").click(function(){
            $("#formulario_editar_usuari_extern_cabecera").trigger("reset");
            $("#formulario_editar_usuari_extern_cabecera").attr("action","/gestor_UsuariExtern/");
            $("#formulario_editar_usuari_extern_cabecera").attr("method","POST");
            mostrar_dialog_cabecera("editar_usuari_extern_cabecera");
    //	    $("#editar_organismes_participants").attr("method","POST")
        });

        /// AJAX
        $("#formulario_editar_usuari_extern_cabecera").submit(function(e){
        var form = $(this);
        if(validar_form(form)){
            $.ajax({
                        url: form.attr('action'),
                        type: form.attr('method'),
                        data: form.serialize(),
                        success: function(result) {
                             mostrar_dialog_cabecera("table_usuaris_externs_cabecera");
                             usuaris_externs_cabecera.ajax.reload();
                        }

            });
        }
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    /////////////////////////////////////


    ////////DIALOGS CABECERA
	$("#dialogs_cabecera").dialog({
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


	$("#dialogs_cabecera").dialog("close");


});

function mostrar_dialog_cabecera(dialog){
//    var titulo = "";
    $("#dialogs_cabecera").dialog("open");
    $(".dialogcabecera").each(function(){
        $(this).hide();
        if($(this).attr("id")==dialog){
             $(this).show();
    //         titulo = $(this).attr("title");
             $("#dialogs_cabecera").dialog({"title":$(this).attr("title")});
        }
    });
    $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();

}