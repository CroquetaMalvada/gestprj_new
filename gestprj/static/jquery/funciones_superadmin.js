var usuaris_xarxa_sense_assignar;
var usuaris_xarxa_cabecera;

$(document).ready(function(){
    /////IDIOMA DATATABLES
    var opciones_idioma = {
        "decimal":        separador_decimales,
        "thousands":      separador_miles,
        "emptyTable":     "No s'han trobat dades",
        "info":           "", //Mostrant d'_START_ a _END_ de _TOTAL_ resultats
        "infoEmpty":      "0 resultats",
        "infoFiltered":   "(filtrats d'un total de _MAX_)",
        "infoPostFix":    "",
        "lengthMenu":     "Show _MENU_ entries",
        "loadingRecords": "Carregant...",
        "processing":     "Processant...",
        "search":         "Buscar:",
        "zeroRecords":    "No s'han trobat resultats",
        "paginate": {
            "first":      "Primer",
            "last":       "Últim",
            "next":       "Següent",
            "previous":   "Anterior"
        },
        "aria": {
            "sortAscending":  ": activar per ordenar de forma ascendent",
            "sortDescending": ": activar per ordenar de forma descendent"
        }
    }


//    usuaris_xarxa_cabecera = $("#table_usuaris_xarxa_cabecera").children("table").DataTable({
//        ajax: {
//            url: '/json_vacio_results/',
//            dataSrc: ""
//        },
//        columns:[
//            {'data': 'url'},
//            {'data': 'nom_xarxa'},
//            {'data': 'id_usuari'},
//            {"render": function(){return '<input type="text" class="nom_usuari_creaf_input"/>';}},
//            {"render": function(){return '<a class="btn btn-success afegir_usuaris_xarxa_sense_assignar" title="Afegir" href="#"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></a>';}}
//            //{"render": function(){return '<a class="btn btn-info editar_usuaris_xarxa_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
//            //{"render": function(){return '<a class="btn btn-danger eliminar_usuaris_xarxa_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
//        ],
//        columnDefs:[
//            {"visible":false,"targets":[0]},
//            { "width": "5%", "targets": [3,4] }
//        ],
//        scrollY:        '70vh',
//        scrollCollapse: true,
//        paging:         false,
//        autowidth:      true,
//        overflow:       "auto",
//        language: opciones_idioma
//    });

    usuaris_xarxa_sense_assignar = $("#table_usuaris_xarxa_sense_assignar").children("table").DataTable({
        ajax: {
            url: '/json_vacio_results/',
            dataSrc: ''
        },
        columns:[
            {'data': 'id'},
            {'data': 'nom_usuari'},
            {"render": function(){return '<input type="text" class="nom_usuari_creaf_input"/>';}},
            {"render": function(){return '<a class="btn btn-success afegir_usuaris_xarxa_sense_assignar" title="Afegir" href="#"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></a>';}}
//            {"render": function(){return '<input class="nom_usuari_xarxa_input"/>';}},
        ],
//        columnDefs:[
////            {"visible":false,"targets":[0]},
//            { "width": "5%", "targets": [2] }
//        ],
        scrollY:        '70vh',
        scrollCollapse: true,
        paging:         false,
        autowidth:      true,
        overflow:       "auto",
        language: opciones_idioma
    });

//
    $(document).on( 'click', '.afegir_usuaris_xarxa_sense_assignar', function (){
                var idusr = usuaris_xarxa_sense_assignar.row(".selected").data()["id"];
                var nomusr_creaf = $(usuaris_xarxa_sense_assignar.row(".selected").nodes()).find(".nom_usuari_creaf_input").val();
                var nomusr_xarxa = $(usuaris_xarxa_sense_assignar.row(".selected").nodes()).find(".nom_usuari_xarxa_input").val();
                if(nomusr_creaf!=""){
                    $.ajax({
                        url: "/afegir_usuari_xarxa_sense_assignar/",
                        type: "POST",
                        data: {"id":idusr, "nom_usuari":nomusr_creaf,"nom_xarxa":nomusr_xarxa},
                        success: function(result) {
                            usuaris_xarxa_sense_assignar.ajax.reload();
                            alert("Usuari afegit amb éxit.")
                        }
                     });
                 }else{
                    alert("Error: Camp incorrecte.")
                 }
    });

///////// USUARIS XARXA
//        //////EDITAR
//        $(document).on( 'click', '.editar_usuari_extern_cabecera', function (){
//    //        var load = loading("Carregant...");
//            var form = $("#formulario_editar_usuari_extern_cabecera");
//            $("#formulario_editar_usuari_extern_cabecera").attr("action",usuaris_externs_cabecera.row(".selected").data()["url"]);
//            $("#formulario_editar_usuari_extern_cabecera").attr("method","PUT");
//
//            $.get(usuaris_externs_cabecera.row(".selected").data()["url"],function( data ){
//                form.children("[name='nom_xarxa']").val(data["nom_xarxa"]);
//                form.children("[name='adreca']").val(data["adreca"]);
//            }).done(function( data ){});
//            usuaris_externs_cabecera.ajax.reload();
//            mostrar_dialog_cabecera("editar_usuari_extern_cabecera");
//
//        });
//
//         $(document).on( 'click', '.eliminar_usuari_extern_cabecera', function (){
//
//            $.confirm({
//                title: 'Confirmació',
//                content: "Segur que vols eliminar aquest element?",
//                confirmButton: 'Si',
//                cancelButton: 'No',
//                confirmButtonClass: 'btn-info',
//                cancelButtonClass: 'btn-danger',
//                closeIcon: false,
//                confirm: function(){
//                $.ajax({
//                    url: usuaris_externs_cabecera.row(".selected").data()["url"],
//                    type: "DELETE",
//                    success: function(result) {
//                        actualizar_usuaris_externs_select();
//                        usuaris_externs_cabecera.ajax.reload();
//                    }
//                 });
//                },
//                cancel: function(){
//                }
//            });
//        });
//
//            //// CREAR UNO
//            $("#editar_personal_extern_crear_cabecera").click(function(){
//                $("#formulario_editar_usuari_extern_cabecera").trigger("reset");
//                $("#formulario_editar_usuari_extern_cabecera").attr("action","/gestor_UsuariExtern/");
//                $("#formulario_editar_usuari_extern_cabecera").attr("method","POST");
//                mostrar_dialog_cabecera("editar_usuari_extern_cabecera");
//        //	    $("#editar_organismes_participants").attr("method","POST")
//            });

///////////////////////////

});

//function dialog_usuaris_xarxa_cabecera(){
//    usuaris_xarxa_cabecera.ajax.url("/llista_Usuaris_xarxa/");
//    usuaris_xarxa_cabecera.ajax.reload();
//    mostrar_dialog_cabecera("table_usuaris_xarxa_cabecera");
//}

function dialog_usuaris_xarxa_sense_assignar(){
    usuaris_xarxa_sense_assignar.ajax.url("/llista_usuaris_xarxa_sense_assignar/");
    usuaris_xarxa_sense_assignar.ajax.reload();
    mostrar_dialog_cabecera("table_usuaris_xarxa_sense_assignar");
}