$(document).ready(function(){
    organismes = crear_datatable(3);
    proyectos_user = crear_datatable(4);
    personal_creaf = crear_datatable(5);
    usuaris_creaf = crear_datatable(6);
    personal_extern = crear_datatable(7);
    usuaris_externs = crear_datatable(8);
    justificacions_personal = crear_datatable(9);

        //////////OPERACIONES ORGANISMES PARTICIPANTS

        $(document).on('click','.afegir_a_centres_participants',function(){
    //        if($.inArray(organismes.row('.selected').data()["nom_organisme"],centres_participants.column(1).data()) != -1){//si ya está ese organismo en los participantes
    //            alert("Aquest organisme ja està participant en aquest projecte.");
    //        }else{
                 $.ajax({
                    url: "/gestor_centresPart/",
                    type: "POST",
                    data: {
                        "id_projecte":id_prj,
                        "id_organisme":organismes.row('.selected').data()["id_organisme"]
                    },
                    success: function(result) {
    //                     $("#dialogs").dialog("close");
                            organismes.$('tr.selected').hide("highlight",{color:"green"},function(){
                            refrescaTabla(1);
                            refrescaTabla(2);
                         });

                    }
                 });
    //         }
        });


        $("#table_centres_participants").on( 'click', '.quitar_organisme_participant', function () {
        $.ajax({
            url: centres_participants.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                centres_participants.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(1);
                    refrescaTabla(2);
                });
            }
         });
    });


    ////////////////////// ORGANISMES

    $(document).on( 'click', '.editar_organisme', function (){

        var form = $("#formulario_editar_organismes_participants");
        $("#formulario_editar_organismes_participants").attr("action",organismes.row(".selected").data()["url"]);
	    $("#formulario_editar_organismes_participants").attr("method","PUT");
//        loading("Actualitzant");
        $.get(organismes.row(".selected").data()["url"],function( data ){
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

        mostrar_dialog("editar_organismes_participants");

    });

    $(document).on( 'click', '.eliminar_organisme', function (){
        $.ajax({
            type: "DELETE",
            url: organismes.row(".selected").data()["url"],
            success: function(result) {
                 organismes.$('tr.selected').hide("highlight",{color:"green"},function(){
                    refrescaTabla(1);
                    refrescaTabla(2);
                 });
            }
         });
    });
    /////////////////////////////////////
        ///////////////// OPERACIONES PERSONAL CREAF

    $("#table_personal_creaf").on( 'click', '.quitar_personal_creaf', function () {
        $.ajax({
            url: personal_creaf.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                personal_creaf.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(3);
                    refrescaTabla(4);
                });
            }
         });
    });

    $(document).on('click','.afegir_a_personal_creaf',function(){
                 $.ajax({
                    url: "/gestor_PersonalCreaf/",
                    type: "POST",
                    data: {
                        "id_projecte":id_prj,
                        "id_usuari":usuaris_creaf.row('.selected').data()["id_usuari"]
                    },
                    success: function(result) {
    //                     $("#dialogs").dialog("close");
                        usuaris_creaf.$('tr.selected').hide("highlight",{color:"green"},function(){
                            refrescaTabla(3);
                            refrescaTabla(4);
                        });

                    }
                 });
    //         }
        });

    $(document).on( 'click', '.eliminar_usuari_creaf', function (){
        $.ajax({
            url: usuaris_creaf.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                 refrescaTabla(3);
                 refrescaTabla(4);
            }
         });
    });

    $(document).on( 'click', '.editar_usuari_creaf', function (){

        var form = $("#formulario_editar_usuari_creaf");
        $("#formulario_editar_usuari_creaf").attr("action",usuaris_creaf.row(".selected").data()["url"]);
	    $("#formulario_editar_usuari_creaf").attr("method","PUT");

        $.get(usuaris_creaf.row(".selected").data()["url"],function( data ){
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

        mostrar_dialog("editar_usuari_creaf");
    });
    /////////////////////////////////////
    ///////////////// OPERACIONES PERSONAL EXTERN

    $("#table_personal_extern").on( 'click', '.quitar_personal_extern', function () {
        $.ajax({
            url: personal_extern.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                personal_extern.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(5);
                    refrescaTabla(6);
                });
            }
         });
    });

    $(document).on('click','.afegir_a_personal_extern',function(){
    //        if($.inArray(organismes.row('.selected').data()["nom_organisme"],centres_participants.column(1).data()) != -1){//si ya está ese organismo en los participantes
    //            alert("Aquest organisme ja està participant en aquest projecte.");
    //        }else{
                 $.ajax({
                    url: "/gestor_PersonalExtern/",
                    type: "POST",
                    data: {
                        "id_projecte":id_prj,
                        "id_usuari_extern":usuaris_externs.row('.selected').data()["id_usuari_extern"]
                    },
                    success: function(result) {
    //                     $("#dialogs").dialog("close");
                        usuaris_externs.$('tr.selected').hide("highlight",{color:"green"},function(){
                            refrescaTabla(5);
                            refrescaTabla(6);
                        });

                    }
                 });
    //         }
        });

    $(document).on( 'click', '.eliminar_usuari_extern', function (){
            $.ajax({
                url: usuaris_externs.row(".selected").data()["url"],
                type: "DELETE",
                success: function(result) {
                     refrescaTabla(5);
                     refrescaTabla(6);
                }
             });
    });

    $(document).on( 'click', '.editar_usuari_extern', function (){

        var form = $("#formulario_editar_usuari_extern");
        $("#formulario_editar_usuari_extern").attr("action",usuaris_externs.row(".selected").data()["url"]);
	    $("#formulario_editar_usuari_extern").attr("method","PUT");

        $.get(usuaris_externs.row(".selected").data()["url"],function( data ){
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
        }).done(function( data ){$(document).find("#loading").dialog("close");});

        mostrar_dialog("editar_usuari_extern");

    });
    /////////////////////////////////////
    ////////// OPERACIONES JUSTIFICACIONES PERSONAL
    $(document).on( 'click', '.mostrar_justific_personal', function (){
	    id_current_perso_creaf = personal_creaf.row(".selected").data()["id_perso_creaf"];
        justificacions_personal.ajax.url('/show_justificPersonal/'+id_current_perso_creaf);
	    refrescaTabla(7);
	    $("#table_justificacions_personal p").text(personal_creaf.row(".selected").data()["nom_usuari"]);
	    mostrar_dialog("table_justificacions_personal");
	});

    $("#table_justificacions_personal").on( 'click', '.editar_justificacio_personal', function (){
        var form = $("#formulario_editar_justificacio_personal");
        $("#formulario_editar_justificacio_personal").attr('action',justificacions_personal.row(".selected").data()["url"]);
	    $("#formulario_editar_justificacio_personal").attr("method","PUT");

        $.get(justificacions_personal.row(".selected").data()["url"],function( data ){
            form.children("[name='data_inici']").val(data["data_inici"]);
            form.children("[name='data_fi']").val(data["data_fi"]);
            form.children("[name='id_feina']").val(data["id_feina"]);
            form.children("[name='hores']").val(data["hores"]);
            form.children("[name='cost_hora']").val(data["cost_hora"]);
        });
	    mostrar_dialog("editar_justificacio_personal");
    });

    $("#table_justificacions_personal").on( 'click', '.eliminar_justificacio_personal', function () {
        $.ajax({
            url: justificacions_personal.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    justificacions_personal.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(7);
                });
            }
         });
    });

    /////////////////////////////////////
});