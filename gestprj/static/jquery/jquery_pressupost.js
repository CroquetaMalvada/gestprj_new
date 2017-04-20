$(document).ready(function(){
    pressupost = crear_datatable(14);
    periodicitat_pressupost = crear_datatable(15);
    periodicitat_partida = crear_datatable(16); // se crea vacia,pero se actualiza cuando se acaba de crear la de pressupost
    desglossament = crear_datatable(17);

    $("#data_periodicitat_pressupost_inici").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_periodicitat_pressupost_fi").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});

     ///////////////// OPERACIONES PRESSUPOST
    $("#afegir_pressupost").click(function(){
	    $("#formulario_pressupost").trigger("reset");
	    $("#formulario_pressupost").attr("action","/gestor_Pressupost/");
	    $("#formulario_pressupost").attr("method","POST");
	    $("#formulario_pressupost").show();
	    mostrar_dialog("editar_pressupost");
	});

    $("#table_pressupost").on( 'click', '.editar_pressupost', function (){
        var form = $("#formulario_pressupost");
        $("#formulario_pressupost").attr('action',pressupost.row(".selected").data()["url"]);
	    $("#formulario_pressupost").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(pressupost.row(".selected").data()["url"],function( data ){
            form.children("[name='id_concepte_pres']").val(data["id_concepte_pres"]);
            form.children("[name='import_field']").val(data["import_field"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_pressupost");
    });

    $("#table_pressupost").on( 'click', '.eliminar_pressupost', function () {
        var partida_id = pressupost.row(".selected").data()["id_part"];
        $.ajax({
            url: pressupost.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    pressupost.$('tr.selected').hide("highlight",{color:"red"},function(){
                        refrescaTabla(12);
                         refrescaTabla(14);
                    });
            }
        });
    });

    ///AJAX
    $("#formulario_pressupost").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                        periodicitat_pressupost.rows().every(function(rowidx,tableloop,rowloop){
                            $.ajax({
                                url: "/gestor_PeriodicitatPartida/",
                                type: "POST",
                                datatype:'json',
                                data: {'id_partida':result['id_part'] ,'id_periodicitat':periodicitat_pressupost.row(rowidx).data()["id_perio"],'import_field':0},
    //                            'id_partida='+id_current_partida+'&id_periodicitat='+form.children("[name='id_concepte_pres']").val()+'&import_field=0',
                                success: function(result) {
                                     cerrar_dialog();
                                     refrescaTabla(13);
                                     refrescaTabla(14);
                                },
                                error: function(error){
                                    console.log(error);
                                }
                            });
                        });
                         cerrar_dialog();
                         refrescaTabla(12);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

 ///////////////// OPERACIONES PERIODICITAT PRESSUPOST
    $("#afegir_periodicitat_pressupost").click(function(){
	    $("#formulario_periodicitat_pressupost").trigger("reset");
	    $("#formulario_periodicitat_pressupost").attr("action","/gestor_PeriodicitatPres/");
	    $("#formulario_periodicitat_pressupost").attr("method","POST");
	    $("#formulario_periodicitat_pressupost").show();
	    mostrar_dialog("editar_periodicitat_pressupost");
	});

    $("#table_periodicitat_pressupost").on( 'click', '.editar_periodicitat_pressupost', function (){
        var form = $("#formulario_periodicitat_pressupost");
        $("#formulario_periodicitat_pressupost").attr('action',periodicitat_pressupost.row(".selected").data()["url"]);
	    $("#formulario_periodicitat_pressupost").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(periodicitat_pressupost.row(".selected").data()["url"],function( data ){
            form.children("[name='etiqueta']").val(data["etiqueta"]);
            form.children("[name='data_inicial']").val(data["data_inicial"]);
            form.children("[name='data_final']").val(data["data_final"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_periodicitat_pressupost");
    });

    $("#table_periodicitat_pressupost").on( 'click', '.eliminar_periodicitat_pressupost', function () {
        $.ajax({
            url: periodicitat_pressupost.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    periodicitat_pressupost.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(13);
                    refrescaTabla(14);
                });
            }
         });
    });
    ///AJAX
    $("#formulario_periodicitat_pressupost").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(response) {
//                          alert(response["id_perio"]);
                        pressupost.rows().every(function(rowidx,tableloop,rowloop){
                            $.ajax({
                                url: "/gestor_PeriodicitatPartida/",
                                type: "POST",
                                datatype:'json',
                                data: {'id_partida':pressupost.row(rowidx).data()["id_part"],'id_periodicitat':response["id_perio"],'import_field':0},
    //                            'id_partida='+id_current_partida+'&id_periodicitat='+form.children("[name='id_concepte_pres']").val()+'&import_field=0',
                                success: function(result) {
                                     cerrar_dialog();
                                     refrescaTabla(13);
                                     refrescaTabla(14);
                                },
                                error: function(error){
                                console.log(error);
                                }
                            });

                        });
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

///////////////// OPERACIONES PERIODICITAT PARTIDA
//    $("#afegir_periodicitat_partida").click(function(){
//	    $("#formulario_periodicitat_partida").trigger("reset");
//	    $("#formulario_periodicitat_partida").attr("action","/gestor_PeriodicitatPartida/");
//	    $("#formulario_periodicitat_partida").attr("method","POST");
//	    $("#formulario_periodicitat_partida").show();
//	    mostrar_dialog("editar_periodicitat_partida");
//	});

    $("#table_periodicitat_partida").on( 'click', '.editar_periodicitat_partida', function (){
        var form = $("#formulario_periodicitat_partida");
        $("#formulario_periodicitat_partida").attr('action',periodicitat_partida.row(".selected").data()["url"]);
	    $("#formulario_periodicitat_partida").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(periodicitat_partida.row(".selected").data()["url"],function( data ){
            form.children("[name='import_field']").val(data["import_field"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_periodicitat_partida");
    });

//    $("#table_periodicitat_partida").on( 'click', '.eliminar_periodicitat_partida', function () {
//        $.ajax({
//            url: periodicitat_partida.row(".selected").data()["url"],
//            type: "DELETE",
//            success: function(result) {
//                    periodicitat_partida.$('tr.selected').hide("highlight",{color:"red"},function(){
//                    refrescaTabla(13);
//                });
//            }
//         });
//    });
    ///AJAX
    $("#formulario_periodicitat_partida").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_partida="+periodicitat_partida.row(".selected").data()["id_partida"]+"&id_periodicitat="+periodicitat_partida.row(".selected").data()["id_periodicitat"],
                    success: function(response) {
                                 cerrar_dialog();
                                 refrescaTabla(14);
                    }
        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

    ///////////////// DESGLOSSAMENT
    $("#afegir_desglossament").click(function(){
	    $("#formulario_desglossament").trigger("reset");
	    $("#formulario_desglossament").attr("action","/gestor_Desglossament/");
	    $("#formulario_desglossament").attr("method","POST");
	    $("#formulario_desglossament").show();
	    mostrar_dialog("editar_desglossament");
	    alert(id_current_partida);
	});

    $("#table_desglossament").on( 'click', '.editar_desglossament', function (){
        var form = $("#formulario_desglossament");
        $("#formulario_desglossament").attr('action',desglossament.row(".selected").data()["url"]);
	    $("#formulario_desglossament").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(desglossament.row(".selected").data()["url"],function( data ){
            form.children("[name='compte']").val(data["id_concepte_pres"]);
            form.children("[name='id_compte']").val(data["id_compte"]);
            form.children("[name='import_field']").val(data["import_field"]);
            form.children("[name='desc_compte']").val(data["desc_compte"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_desglossament");
    });

    $("#table_desglossament").on( 'click', '.eliminar_desglossament', function () {
        var partida_id = desglossament.row(".selected").data()["id_part"];
        $.ajax({
            url: desglossament.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    desglossament.$('tr.selected').hide("highlight",{color:"red"},function(){
                        refrescaTabla(15);
                    });
            }
        });
    });

    ///AJAX
    $("#formulario_desglossament").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj+"&id_partida="+id_current_partida,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(15);
                    },
                    error: function(result){
                        console.log(result);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

});

