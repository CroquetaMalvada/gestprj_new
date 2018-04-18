$(document).ready(function(){
//    compromes = crear_datatable(20);
    compromes_personal = crear_datatable(20);

    $("#data_compromes_inici").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#data_compromes_fi").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});


    ///////////////// OPERACIONES COMPROMES PERSONAL
    $("#afegir_compromes_personal").click(function(){
	    $("#formulario_compromes_personal").trigger("reset");
	    $("#formulario_compromes_personal").attr("action","/gestor_CompromesPersonal/");
	    $("#formulario_compromes_personal").attr("method","POST");
	    $("#formulario_compromes_personal").show();
	    mostrar_dialog("editar_compromes_personal");
	});

    $("#table_compromes_personal").on( 'click', '.editar_compromes_personal', function (){
        var form = $("#formulario_compromes_personal");
        $("#formulario_compromes_personal").attr('action',compromes_personal.row(".selected").data()["url"]);
        $("#formulario_compromes_personal").attr("method","PUT");

        var load = loading("Carregant...");
        $.get(compromes_personal.row(".selected").data()["url"],function( data ){
            form.children("[name='compte']").val(data["compte"]);
            form.children("[name='descripcio']").val(data["descripcio"]);
            form.children("[name='cost']").val(formatnumber( data["cost"], separador_miles, separador_decimales, 2 ));
            form.children("[name='data_inici']").val(data["data_inici"]);
            form.children("[name='data_fi']").val(data["data_fi"]);
        }).done(function( data ){load.close();});
        mostrar_dialog("editar_compromes_personal");
    });

    $("#table_compromes_personal").on( 'click', '.eliminar_compromes_personal', function () {

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
                    url: compromes_personal.row(".selected").data()["url"],
                    type: "DELETE",
                    success: function(result) {
                            compromes_personal.$('tr.selected').hide("highlight",{color:"red"},function(){
                            refrescaTabla(20);
                        });
                    }
                 });
            },
            cancel: function(){
            }
        });
    });
    ///AJAX
    $("#formulario_compromes_personal").submit(function(e){
        var form = $(this);
        if(validar_form(form)){
            $.ajax({
                        url: form.attr('action'),
                        type: form.attr('method'),
                        data: form.serialize()+"&id_projecte="+id_prj,
                        success: function(result) {
                             cerrar_dialog();
                             refrescaTabla(20);
                        }

            });
        }
        e.preventDefault(); //para no ejecutar el actual submit del form
    });
    ///
    //////////////////////////////////////////////////////

//    $("#table_compromes_partida").find("tbody").on( 'click', 'tr', function () {
//                id_current_partida_compromes=$("#table_pressupost").DataTable().row(".selected").data()["id_partida"];
////                $("#nombre_partida").html($("#table_pressupost").DataTable().row(".selected").data()["nom_partida"]);
////                refrescaTabla(14);
//    });
//    $("#table_compromes").find("tbody").on( 'click', '.observar_compromes', function () {
//                refrescaTabla(21);
//                mostrar_dialog("compromes_partida");
//    });
//    $.ajax({
//        url: '/show_compromes_personal/'+id_prj,
////        type: "POST",
////        data: {
////            "id_projecte":id_prj,
////            "id_organisme":organismes.row('.selected').data()["id_organisme"]
////        },
//        success: function(result) {
////                     $("#dialogs").dialog("close");
////                mostrar_dialog("compromes_personal");
////                organismes.$('tr.selected').hide("highlight",{color:"green"},function(){
////                refrescaTabla(1);
////                refrescaTabla(2);
////             });
//
//        }
//     });

//    var guardando=0;
//     $(".guardar_compromes_personal").click(function(){
//        if(guardando==0){
//            guardando=1;
//            $(this).parent("tr")
//            $.ajax({
//                    url: '/show_compromes_personal/'+id_prj,
////                    type: "POST",
////                    data: {
////                        "id_projecte":id_prj,
////                        "compte":compromes_personal.row('.selected').data()["id_organisme"]
////                    },
//                    success: function(result) {
//            //                     $("#dialogs").dialog("close");
//                            mostrar_dialog("compromes_personal");
//            //                organismes.$('tr.selected').hide("highlight",{color:"green"},function(){
//            //                refrescaTabla(1);
//            //                refrescaTabla(2);
//            //             });
//
//                    }
//                 });
//
//        }
//
//	});

});


function calcular_compromes_personal(){
    compromes_personal.rows().every(function(rowidx){
        var fecha_actual=$.datepicker.formatDate('yy-mm-dd', new Date());

        var coste = compromes_personal.cell(rowidx,4).data();
        var fecha_ini = new Date(compromes_personal.cell(rowidx,5).data());
        var fecha_fin = new Date(compromes_personal.cell(rowidx,6).data());
        var dif = new Date(fecha_fin-fecha_ini);
        var duracion_total = dif / 1000 / 60 / 60 / 24; // en dias
        var fecha_calculo = new Date(fecha_actual); //el ultimo dia del mes anterior
        fecha_calculo.setDate(1); //la ponemos al dia 1
        fecha_calculo.setHours(-1);// y le restamos una hora
        fecha_calculo_string=$.datepicker.formatDate('yy-mm-dd',fecha_calculo)
        fecha_calculo = new Date(fecha_calculo_string); //la formateamos
        dif=new Date(fecha_fin - fecha_calculo);
//        console.log(compromes_personal.cell(rowidx,5).data());
//        console.log(fecha_fin);
//        console.log(fecha_calculo);
        var duracion_pendiente = dif/ 1000 / 60 / 60 / 24; // en dias
        var comprometido = duracion_pendiente * (coste/30);
        var comprometido = duracion_pendiente * (coste/30);

//        alert(fecha_fin);
//        alert(fecha_calculo);
        // datos no visibles
//        compromes_personal.cell(rowidx,7).data(duracion_total);
//        compromes_personal.cell(rowidx,8).data(fecha_actual);
//        compromes_personal.cell(rowidx,9).data(duracion_pendiente);
//        compromes_personal.cell(rowidx,10).data(comprometido);

        $(compromes_personal.cell(rowidx,7).node()).html(duracion_total);
        $(compromes_personal.cell(rowidx,8).node()).html(fecha_calculo_string);
        $(compromes_personal.cell(rowidx,9).node()).html(duracion_pendiente);
        $(compromes_personal.cell(rowidx,10).node()).html(formatnumber( comprometido, separador_miles, separador_decimales, 2 ));

    })
}