$(document).ready(function(){
    organismes_fin = crear_datatable(10);
    organismes_rec = crear_datatable(11);
    justificacions_internes = crear_datatable(12);
    renovacions = crear_datatable(13);


    $("#id_data_assentament").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_renovacio_inici").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_renovacio_fi").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});

    /////////////////////////////////////
    ///////////////// OPERACIONES ORGANISMES FINANCADORS
    $("#afegir_organisme_fin").click(function(){
	    $("#formulario_organismes_fin").trigger("reset");
	    $("#formulario_organismes_fin").attr("action","/gestor_OrganismesFin/");
	    $("#formulario_organismes_fin").attr("method","POST");
	    $("#formulario_organismes_fin").show();
	    mostrar_dialog("editar_organisme_fin");
	});

    $("#table_organismes_fin").on( 'click', '.editar_organisme_fin', function (){
        var form = $("#formulario_organisme_fin");
        $("#formulario_organisme_fin").attr('action',organismes_fin.row(".selected").data()["url"]);
	    $("#formulario_organisme_fin").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(organismes_fin.row(".selected").data()["url"],function( data ){
            form.children("[name='id_organisme']").val(data["id_organisme"]);
            form.children("[name='import_concedit']").val(data["import_concedit"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_organisme_fin");
    });

    $("#table_organismes_fin").on( 'click', '.eliminar_organisme_fin', function () {
        $.ajax({
            url: organismes_fin.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    organismes_fin.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(8);
                });
            }
         });
    });
    ///AJAX
    $("#formulario_organisme_fin").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(8);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

/////////////////////////////////////
    ///////////////// OPERACIONES ORGANISMES RECEPTORS
    $("#afegir_organisme_rec").click(function(){
	    $("#formulario_organismes_rec").trigger("reset");
	    $("#formulario_organismes_rec").attr("action","/gestor_OrganismesRec/");
	    $("#formulario_organismes_rec").attr("method","POST");
	    $("#formulario_organismes_rec").show();
	    mostrar_dialog("editar_organisme_rec");
	});

    $("#table_organismes_rec").on( 'click', '.editar_organisme_rec', function (){
        var form = $("#formulario_organisme_rec");
        $("#formulario_organisme_rec").attr('action',organismes_rec.row(".selected").data()["url"]);
	    $("#formulario_organisme_rec").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(organismes_rec.row(".selected").data()["url"],function( data ){
            form.children("[name='id_organisme']").val(data["id_organisme"]);
            form.children("[name='import_rebut']").val(data["import_rebut"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_organisme_rec");
    });

    $("#table_organismes_rec").on( 'click', '.eliminar_organisme_rec', function () {
        $.ajax({
            url: organismes_rec.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    organismes_rec.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(9);
                });
            }
         });
    });


    /// AJAX
    $("#formulario_organisme_rec").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(9);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

/////////////////////////////////////
    ///////////////// OPERACIONES ORGANISMES RECEPTORS
    $("#afegir_justif_interna").click(function(){
	    $("#formulario_justif_interna").trigger("reset");
	    $("#formulario_justif_interna").attr("action","/gestor_JustificInternes/");
	    $("#formulario_justif_interna").attr("method","POST");
	    $("#formulario_justif_interna").show();
	    mostrar_dialog("editar_justif_interna");
	});

    $("#table_justificacions_internes").on( 'click', '.editar_justifInterna', function (){
        var form = $("#formulario_justif_interna");
        $("#formulario_justif_interna").attr('action',justificacions_internes.row(".selected").data()["url"]);
	    $("#formulario_justif_interna").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(justificacions_internes.row(".selected").data()["url"],function( data ){
            form.children("[name='data_assentament']").val(data["data_assentament"]);
            form.children("[name='id_assentament']").val(data["id_assentament"]);
            form.children("[name='desc_justif']").val(data["desc_justif"]);
            form.children("[name='import_field']").val(data["import_field"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_justif_interna");
    });

    $("#table_justificacions_internes").on( 'click', '.eliminar_justifInterna', function () {
        $.ajax({
            url: justificacions_internes.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    justificacions_internes.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(10);
                });
            }
         });
    });


    /// AJAX
    $("#formulario_justif_interna").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(10);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

/////////////////////////////////////
    ///////////////// OPERACIONES ORGANISMES RECEPTORS
    $("#afegir_renovacio").click(function(){
	    $("#formulario_renovacio").trigger("reset");
	    $("#formulario_renovacio").attr("action","/gestor_Renovacions/");
	    $("#formulario_renovacio").attr("method","POST");
	    $("#formulario_renovacio").show();
	    mostrar_dialog("editar_renovacio");
	});

    $("#table_renovacions").on( 'click', '.editar_renovacio', function (){
        var form = $("#formulario_renovacio");
        $("#formulario_renovacio").attr('action',renovacions.row(".selected").data()["url"]);
	    $("#formulario_renovacio").attr("method","PUT");

        $(document).find("#loading").dialog("open");
        $.get(renovacions.row(".selected").data()["url"],function( data ){
            form.children("[name='data_inici']").val(data["data_inici"]);
            form.children("[name='data_fi']").val(data["data_fi"]);
            form.children("[name='import_concedit']").val(data["import_concedit"]);
        }).done(function( data ){$(document).find("#loading").dialog("close");});
	    mostrar_dialog("editar_renovacio");
    });

    $("#table_renovacions").on( 'click', '.eliminar_renovacio', function () {
        $.ajax({
            url: renovacions.row(".selected").data()["url"],
            type: "DELETE",
            success: function(result) {
                    renovacions.$('tr.selected').hide("highlight",{color:"red"},function(){
                    refrescaTabla(11);
                });
            }
         });
    });


    /// AJAX
    $("#formulario_renovacio").submit(function(e){
        var form = $(this);
        $.ajax({
                    url: form.attr('action'),
                    type: form.attr('method'),
                    data: form.serialize()+"&id_projecte="+id_prj,
                    success: function(result) {
                         cerrar_dialog();
                         refrescaTabla(11);
                    }

        });
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///

////////////////////////////////

/////////////////OPERACIONES INPUTS(CANON E IVA)

$("#id_canon_oficial").change(function(){
    actualizar_canoniva();
});
$("#id_percen_canon_creaf").change(function(){
    actualizar_canoniva();
});
$("#id_percen_iva").change(function(){
    actualizar_canoniva();
});


//var intervalo = setInterval(function(){
//    if(renovacions_init==true){
//        actualizar_canoniva();
//        clearInterval(intervalo);
//    }
//},1000);


//renovacions_init.on(true,function(){
//    alert( 'DataTables has finished its initialisation.' );
//    actualizar_canoniva();
//});
///////////////////////////////////////////////

});

function cerrar_dialog(){
    $("#dialogs").dialog("close");
}

function actualizar_canoniva(){
                        var tabla = renovacions;

                        $("#total_concedit_renovacio").val(tabla.column( 4 ).data().sum());
                        $( tabla.column( 4 ).footer() ).find("#total_concedit_renovacio").val($("#total_concedit_renovacio").val());///este es para que se vea el resultado

                        ///quizas esto se pueda poner abajo,ya que no son ni de la tabla
                        var canon_oficial_per = ( $("#id_canon_oficial").val() / $("#total_concedit_renovacio").val() ) * ( 100 * ( 1+$("#id_percen_iva").val()/100 ) ) ;
                        $("#canon_oficial_per").val(canon_oficial_per);

                        var canon_creaf_eur = ( $("#total_concedit_renovacio").val() * $("#id_percen_canon_creaf").val() ) / ( 100 * ( 1+$("#id_percen_iva").val()/100 ) ) ;
                        $("#canon_creaf_eur").val(canon_creaf_eur);

                        var diferencia_per = $("#canon_oficial_per").val() - $("#id_percen_canon_creaf").val();
                        $("#diferencia_per").val(diferencia_per);

                        var diferencia_eur =  $("#id_canon_oficial").val() - $("#canon_creaf_eur").val();
                        $("#diferencia_eur").val(diferencia_eur);

                        var iva_eur = ( $("#total_concedit_renovacio").val() * $("#id_percen_iva").val() ) / ( 100 * ( 1+$("#id_percen_iva").val()/100 ) ) ;
                        $("#iva_eur").val(iva_eur);

                            ////CAMPOS DE LA TABLA
                        tabla.rows().every(function(rowidx,tableloop,rowloop){
                                var iva = tabla.cell(rowidx,4).data() - ( tabla.cell(rowidx,4).data() / (1+$("#id_percen_iva").val()/100) );
                                var canon = ( tabla.cell(rowidx,4).data() *  $("#canon_oficial_per").val() ) / (100 * (1+$("#id_percen_iva").val()/100) );

                                tabla.cell(rowidx,5).data(iva);///esta data no se muestra,la guarda datatables
                                $(tabla.cell(rowidx,5).node()).html(iva);

                                tabla.cell(rowidx,6).data(canon);
                                $(tabla.cell(rowidx,6).node()).html(canon);

                                tabla.cell(rowidx,7).data(tabla.cell(rowidx,4).data()-iva-canon);
                                $(tabla.cell(rowidx,7).node()).html(tabla.cell(rowidx,4).data()-iva-canon);


                        });

                        $( tabla.column( 5 ).footer() ).find("#total_iva_renovacio").val(tabla.column( 5 ).data().sum());
                        $( tabla.column( 6 ).footer() ).find("#total_canon_renovacio").val(tabla.column( 6 ).data().sum());
                        $( tabla.column( 7 ).footer() ).find("#total_renovacio").val(tabla.column( 7 ).data().sum());
                        /////
                        $(".max2dec").each(function(){
                            $(this).val( parseFloat($(this).val()).toFixed(2));
                        });
                        $(".max4dec").each(function(){
                            $(this).val( parseFloat($(this).val()).toFixed(4));
                        });
}
