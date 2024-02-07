$(document).ready(function(){
    justificacions_projecte = crear_datatable(18);
    auditories = crear_datatable(19);


    $("#data_justificacio_projecte").datepicker({dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_justificacio_projecte_inici").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_justificacio_projecte_final").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});

    $("#data_auditoria").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_auditoria_inici").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_auditoria_final").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});

    ///////////////// JUSTIFICACIONS PROJECTE
    $("#afegir_justificacio_projecte").click(function(){
	    $("#formulario_justificacions_projecte").trigger("reset");
	    $("#formulario_justificacions_projecte").attr("action","/gestor_JustificacionsProjecte/");
	    $("#formulario_justificacions_projecte").attr("method","POST");
	    $("#formulario_justificacions_projecte").show();
	    mostrar_dialog("editar_justificacio_projecte");
	});

    $("#table_justificacions_projecte").on( 'click', '.editar_justificacio_projecte', function (){
        var form = $("#formulario_justificacio_projecte");
        $("#formulario_justificacio_projecte").attr('action',justificacions_projecte.row(".selected").data()["url"]);
	    $("#formulario_justificacio_projecte").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(justificacions_projecte.row(".selected").data()["url"],function( data ){
            form.children("[name='data_justificacio']").val(data["data_justificacio"]);
            form.children("[name='data_inici_periode']").val(data["data_inici_periode"]);
            form.children("[name='data_fi_periode']").val(data["data_fi_periode"]);
            form.children("[name='comentaris']").val(data["comentaris"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_justificacio_projecte");
    });

    $("#table_justificacions_projecte").on( 'click', '.eliminar_justificacio_projecte', function () {
        $.ajax({
            url: justificacions_projecte.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    justificacions_projecte.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(16);
                });
            }
         });
    });
    ///AJAX
    $("#formulario_justificacio_projecte").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(16);
                    },
                    error:function(error){
                    console.log(error);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

    ///////////////// AUDITORIES
    $("#afegir_auditoria").click(function(){
	    $("#formulario_auditories").trigger("reset");
	    $("#formulario_auditories").attr("action","/gestor_Auditories/");
	    $("#formulario_auditories").attr("method","POST");
	    $("#formulario_auditories").show();
	    mostrar_dialog("editar_auditories");
	});

    $("#table_auditories").on( 'click', '.editar_auditoria', function (){
        var form = $("#formulario_auditories");
        $("#formulario_auditories").attr('action',auditories.row(".selected").data()["url"]);
	    $("#formulario_auditories").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(auditories.row(".selected").data()["url"],function( data ){
            form.children("[name='data_auditoria']").val(data["data_auditoria"]);
            form.children("[name='data_inici_periode']").val(data["data_inici_periode"]);
            form.children("[name='data_fi_periode']").val(data["data_fi_periode"]);
            form.children("[name='comentaris']").val(data["comentaris"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_auditories");
    });

    $("#table_auditories").on( 'click', '.eliminar_auditoria', function () {
        $.ajax({
            url: auditories.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    auditories.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(17);
                });
            }
         });
    });
    ///AJAX
    $("#formulario_auditories").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(17);
                    },
                    error:function(error){
                    console.log(error);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

});