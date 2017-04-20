var table_projectes;
var table_responsables;
var table_comptes;

$(document).ready(function(){
    /////IDIOMA DATATABLES
    var opciones_idioma = {
        "decimal":        ",",
        "emptyTable":     "No s'han trobat dades",
        "info":           "", //Mostrant d'_START_ a _END_ de _TOTAL_ resultats
        "infoEmpty":      "0 resultats",
        "infoFiltered":   "(filtrats d'un total de _MAX_)",
        "infoPostFix":    "",
        "thousands":      ",",
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


   if($("#table_llista_projectes_cont")){//PROYECTOS
        table_projectes= $("#table_llista_projectes_cont").DataTable({
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[4]}
            ],
            language: opciones_idioma
        });
   }

   if($("#table_llista_responsables_cont")){//RESPONSABLES
       table_responsables = $("#table_llista_responsables_cont").DataTable({
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[2]}
            ],
            language: opciones_idioma
        });
   }
    // Al seleccionar un responsable se seleccionarán/deseleccionarán todos los proyectos de los que es responsable
    $(".checkbox_responsable").on("change",function(){
        projectes_de_responsable(this);
    });

   if($("#table_llista_comptes")){//COMPTES
       table_comptes = $("#table_llista_comptes").DataTable({
            ajax: {
                url: '/show_Moviments_Compte/0/0/0', //ej 625012159/01-01-1997/08-02-2017
                dataSrc: '' //como no hay ninguna variable general que contiene el array json,lo dejamos como un string vacio
            },
            columns:[
                {'data': 'Fecha'},
                {'data': 'Asiento'},
                {'data': 'Descripcion'},
                {'data': 'Debe'},
                {'data': 'Haber'},
                {'data': 'Saldo'}
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){return '<h4>'+$("#dialog_llista_comptes").attr("title")+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            }],
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
//            order:          [[ 0, "asc" ]],
//            columnDefs:[
//                { type: 'de_date', targets: 0 }
//            ],
            language: opciones_idioma
        });
   }

///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///Esto sirve para que el campo que contiene una fecha lo detecte como tal para poder asi ordenarlo correctamente por fecha

//   if($(".table_llista_despeses")){// DESPESES
//       $(".table_llista_despeses").DataTable({
//            scrollY:        '60vh',
//            scrollCollapse: true,
//            paging:         false,
//            autowidth:      true,
//            columnDefs: [
//                { type: 'de_date', targets: 0 }
//            ],
//            language: opciones_idioma
//        });
//    }
//
//   if($(".table_llista_ingressos")){// INGRESOS
//       $(".table_llista_ingressos").DataTable({
//            scrollY:        '60vh',
//            scrollCollapse: true,
//            paging:         false,
//            autowidth:      true,
//            columnDefs: [
//                { type: 'de_date', targets: 0 }
//            ],
//            language: opciones_idioma
//        });
//    }

    if($(".table_cont")){// Ojo cambiar la class de las tablas de contabilidad por table_cont y asi poder quitar estas 2 de arriba ^
       $(".table_cont").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 }
            ],
            language: opciones_idioma
        });
    }

//      Ojo esta de abajo no hace falta ya que esta esta declarada mas arriba
//   if($(".table_llista_comptes")){// DIALOG DE LOS MOVIMIENTOS DE COMPTES EN RESUM FITXA MAJOR PER COMPTES
//       $(".table_llista_comptes").DataTable({
//            scrollY:        '60vh',
//            scrollCollapse: true,
//            paging:         false,
//            autowidth:      true,
//            columnDefs: [
//                { type: 'de_date', targets: 0 }
//            ],
//            language: opciones_idioma
//        });
//    }

////////////////////////////
});


function projectes_de_responsable(chk){
    var val = table_responsables.cell(table_responsables.row(".selected").index(),2).data();
    table_projectes.rows().every(function(rowidx,tableloop,rowloop){
        if(table_projectes.cell(rowidx,4).data()==val)
            $(table_projectes.row(rowidx,0).node()).find(":checkbox").prop("checked",$(chk).is(':checked'));
    });
//    console.log(table_responsables.cell(rowidx,2).data());
}