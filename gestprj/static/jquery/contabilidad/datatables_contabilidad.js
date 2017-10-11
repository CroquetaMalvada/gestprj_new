var table_projectes;
var table_responsables;
var table_comptes;

var separador_decimales = ',';
var separador_miles = '.';

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


   if($("#table_llista_projectes_cont")){//PROYECTOS
        table_projectes= $("#table_llista_projectes_cont").DataTable({
            ajax:{
                url: '/show_ProjectesCont/',
                contentType: "application/json;",
                dataSrc: '' //como no hay ninguna variable general que contiene el array json,lo dejamos como un string vacio
            },
            columns:[
                {"render": function(){return '<input name="prj_select" type="checkbox" />';}},
                {'data': 'Codi'},
                {'data': 'Estat'},
                {'data': 'Acronim'},
                {'data': 'Id_resp'}
            ],
            initComplete:function(){
                ////por defecto se muestran los proyectos abiertos
                nomes_oberts();
            },
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[4]},
                {"width": "5%","className":"dt-center", "targets": [0] }
            ],
            dom: 'Bfrtip',
            buttons:[{
                text: '<span class="glyphicon glyphicon-check" aria-hidden="true">  Només Seleccionats</span>',
                action: function(){nomes_seleccionats();}
            },{
                text: '<span class="glyphicon glyphicon-ok" aria-hidden="true">  Només Oberts</span>',
                action: function () {nomes_oberts();}
            },{
                text: '<span class="glyphicon glyphicon-remove" aria-hidden="true">  Només Tancats</span>',
                action: function () {nomes_tancats();}
            },{
                text: '<span class="glyphicon glyphicon-asterisk" aria-hidden="true">  Mostrar Tots</span>',
                action: function () {mostrar_tots();}
            }],
            fnInitComplete:function(){
                var tabla=$(this).DataTable();
                tabla.rows().every(function(rowidx,tableloop,rowloop){
                    // color de celda y bold
                    if(tabla.cell(rowidx,2).data()=='Obert')
                        $(tabla.cell(rowidx,2).node()).addClass("prjabierto");
                    else
                        $(tabla.cell(rowidx,2).node()).addClass("prjcerrado");
                    tabla.cell(rowidx,2).data("<b>"+tabla.cell(rowidx,2).data()+"</b>");
                    //
                    //value de los inputs del proyecto
                    var resp=tabla.cell(rowidx,1).data().substr(0,2);
                    var prj=tabla.cell(rowidx,1).data().substr(2,4);
                    $(tabla.cell(rowidx,0).node()).find(":checkbox").val(resp+"-"+prj);
                    //

                });
                nomes_oberts();
            },
            language: opciones_idioma
        });
   }

   if($("#table_llista_responsables_cont")){//RESPONSABLES
//        alert(llista_responsables);
       table_responsables = $("#table_llista_responsables_cont").DataTable({
            ajax:{
                url: '/show_ResponsablesCont/',
                contentType: "application/json;",
                dataSrc: '' //como no hay ninguna variable general que contiene el array json,lo dejamos como un string vacio
            },
            columns:[
                {"render": function(){return '<input type="checkbox" class="checkbox_responsable responsable_oberts"/>';}},
                {"render": function(){return '<input type="checkbox" class="checkbox_responsable responsable_tancats"/>';}},
                {'data': 'Nom'},
                {'data': 'Id_resp'}
            ],
            stateSave: true,
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 2, "asc" ]],
            columnDefs:[
                {"visible":false,"targets":[3]},
                {"width": "5%","className":"dt-center", "targets": [0,1] }
            ],
            language: opciones_idioma
        });
   }



/////////////////// DATATABLES PARA DIALOGS
   if($("#table_llista_despeses")){//DESPESES COMPTES (DEPENDE DE ESTAT PRESSUPOSTARI PROJECTES)
       table_llista_despeses = $("#table_llista_despeses").DataTable({
            ajax: {
                url: '/show_Despeses_Compte/0/0/0/0', //ej 625012159/01-01-1997/08-02-2017
                contentType: "application/json;",
                dataSrc: '' //como no hay ninguna variable general que contiene el array json,lo dejamos como un string vacio
            },
            columns:[
                {'data': 'Fecha'},
                {'data': 'Asiento'},
                {'data': 'Cuenta'},
                {'data': 'Descripcion'},
                {'data': 'Debe', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){return '<h4>'+$("#dialog_llista_comptes").attr("title")+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==4)// solo nos interesa formatear los numeros de saldo(columna 4)
                                data=parseFloat(data.replace(separador_miles,'').replace(separador_decimales,'.'))//quitamos los separadores de miles y dejamos que los de decimales sean "."
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="E"]', sheet).each(function () {// "E" es la columna en el excel
                          $(this).attr('s', 64);
                   });
                }
            },{
                extend: 'pdf',
                title: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
//            order:          [[ 0, "asc" ]],
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [1,2,4] }
            ],
            language: opciones_idioma
        });
   }

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
                {'data': 'Debe', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                {'data': 'Haber', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                {'data': 'Saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )}
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){return '<h4>'+$("#dialog_llista_comptes").attr("title")+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==3 || column==4 || column==5)
                                data=parseFloat(data.replace(separador_miles,'').replace(separador_decimales,'.'))//quitamos los separadores de miles y dejamos que los de decimales sean "."
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="D"]', sheet).each(function () {
                          $(this).attr('s', 64);
                   });
                }
            },{
                extend: 'pdf',
                title: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return $("#dialog_llista_comptes").attr("title")},
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            scrollY:        '70vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
//            order:          [[ 0, "asc" ]],
            columnDefs:[
                { type: 'de_date', targets: 0 }
            ],
            language: opciones_idioma
        });
   }
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////
///Esto sirve para que el campo que contiene una fecha lo detecte como tal para poder asi ordenarlo correctamente por fecha

    if($(".table_estat_pressupostari")){// ESTAT PRESSUPOSTARI ////////////
       $(".table_estat_pressupostari").each(function(){
           $(this).DataTable({
                ajax:{
                    url:'/json_vacio/',
                    contentType: "application/json;",
                    dataSrc: ''
                },
                scrollY:        '60vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                columnDefs: [
    //                { type: 'de_date', targets: 0 },
                    { type: 'num-fmt', targets: [1,2,4] }
                ],
                columns: [
                    { data:'desc_partida'},
                    { data:'pressupostat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    { data:'gastat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    { data:{'cod':'codigo_entero','id':'id_partida'},"render": function(data){return '<a class="btn btn-info info_compte_pres" id="'+data['id_partida']+'" cod="'+data['codigo_entero']+'"data_min="0" data_max="0" title="Info" href="#"><span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span></a>';}},
                    { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
                ],
                footerCallback: function( tfoot, data, start, end, display ) {
                    var api = this.api();
                    $(this).DataTable().columns( [1,2,4] ).every(function(){
    //                    console.log(this.data());
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                        $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
                    });
                  },
                language: opciones_idioma
            });
        });
    }

//   $.fn.dataTable.render.number( '.', ',', 2, ' $ ' );

    ///////////////////

    if($(".table_llista_despeses")){// DESPESES
       $(".table_llista_despeses").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [6,7,8] }
            ],
            columns: [
                null,
                null,
                null,
                null,
                null,
                null,
                { data:'pagat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'despesa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo disponible', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [7,8] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }


    if($(".table_llista_ingressos")){// INGRESSOS
       $(".table_llista_ingressos").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [4,5] }
            ],
            columns: [
                null,
                null,
                null,
                null,
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [4,5] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_fitxa_major_prj")){// FITXA MAJOR PROJECTES
       $(".table_fitxa_major_prj").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [4,5,6] }
            ],
            columns: [
                null,
                null,
                null,
                null,
                { data:'carrec', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [4,5,6] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_resum_estat_prj_resp")){// ESTAT PROJECTES PER RESPONSABLE
       $(".table_resum_estat_prj_resp").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'num-fmt', targets: [2,3,4,5,6,7,8,9,10] }
            ],
            columns: [
                null,
                null,
                { data:'concedit', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'iva', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canontotal', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingressos', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'pendent', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'despeses', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canonaplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'disponiblecaixa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'disponiblereal', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [2,3,4,5,6,7,8,9,10] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_resum_fitxa_major_prj")){// RESUM FITXA MAJOR PROJECTES PER COMPTES
       $(".table_resum_fitxa_major_prj").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [2,3,5] }
            ],
            columns: [
                null,
                null,
                { data:'carrec', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                null,
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [2,3,5] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_resum_estat_prj")){// RESUM ESTAT PROJECTES
       $(".table_resum_estat_prj").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'num-fmt', targets: [2,3,4,5,6,7,8,9,10] }
            ],
            columns: [
                null,
                null,
                { data:'codi', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'responsable', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'concedit', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'iva', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_total', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingressos', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'pendent', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'despeses', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'disponible_caixa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'disponible_real', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [2,3,4,5,6,7,8,9,10] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_resum_estat_canon")){// Resum Cànon Projectes agrupat per Responsablee
       $(".table_resum_estat_canon").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'num-fmt', targets: [2,3,4,5,6,7,8,9,10,11,12] }
            ],
            columns: [
                null,
                null,
                { data:'base_canon', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen1', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_creaf', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen2', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_oficial', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'dif_canon', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingressos', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen3', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_pendent_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo_canon_oficial', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [2,3,4,5,6,7,8,9,10,11,12] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_comptes_no_assignats")){// COMPTES NO ASSIGNATS
       $(".table_comptes_no_assignats").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            columnDefs: [
                { type: 'num-fmt', targets: [0,2,3,4] }
            ],
            columns: [
                null,
                null,
                { data:'carrec', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $( api.columns( [2,3,4] ).footer() ).find("b").each(function(){
                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
                });
            },
            language: opciones_idioma
        });
    }


////////////////////////////
});

function cargar_ajax_prj(elemento){

    // ESTAT PRESSUPOSTARI ////////////
    if($(elemento).find(".table_estat_pressupostari")){ /// este es el unico que necesita un each ya que puede tener varios periodos
        $(elemento).find(".table_estat_pressupostari").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/show_estat_pres_datos/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }


//       $.fn.dataTable(tabla).api().ajax.url('/show_estat_pres_datos/'+$(tabla).attr("cod"));


//        $(tabla).DataTable({
//                ajax:{
//                    url: '/show_estat_pres_datos/'+$(this).attr("cod"),
//                    contentType: "application/json;",
//                    dataSrc: '' //como no hay ninguna variable general que contiene el array json,lo dejamos como un string vacio
//                },
//                scrollY:        '60vh',
//                scrollCollapse: true,
//                paging:         false,
//                autowidth:      true,
//                columnDefs: [
//    //                { type: 'de_date', targets: 0 },
//                    { type: 'num-fmt', targets: [1,2,4] }
//                ],
//                columns: [
//                    { data:'desc_partida'},
//                    { data:'pressupostat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
//                    { data:'gastat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
//                    { data:{'cod':'codigo_entero','id':'id_partida'},"render": function(data){return '<a class="btn btn-info info_compte_pres" id="'+data['id_partida']+'" cod="'+data['codigo_entero']+'"data_min="0" data_max="0" title="Info" href="#"><span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span></a>';}},
//                    { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
//                ],
//                footerCallback: function( tfoot, data, start, end, display ) {
//                    var api = this.api();
//                    $(this).DataTable().columns( [1,2,4] ).every(function(){
//    //                    console.log(this.data());
//                        var sum = this.data().reduce( function (a,b) {
//                            return parseFloat(a) + parseFloat(b);
//                        },0 ); //OJO cambiar a 2????
//                        $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
//                    });
//                  },
//                language: opciones_idioma
//        });
}

function projectes_de_responsable(chk,tipo){
    var val = table_responsables.cell(table_responsables.row(".selected").index(),3).data();
    table_projectes.rows().every(function(rowidx,tableloop,rowloop){
        if(table_projectes.cell(rowidx,2).data()=="<b>"+tipo+"</b>")
            if(table_projectes.cell(rowidx,4).data()==val)
                $(table_projectes.row(rowidx,0).node()).find(":checkbox").prop("checked",$(chk).is(':checked'));
    });
//    console.log(table_responsables.cell(rowidx,2).data());
}

// esta funcion comprueba si el proyecto pasado es de alguno de los responsables marcados(solo se usa cuando esta marcada la opcion de mostrar solo de responsables)
//function es_de_responsable(){
//}
//
//function nomes_tancats(){
//    table_projectes
//}

function nomes_seleccionats() {
    $("#table_llista_projectes_cont tbody>tr").each(function() { //loop over each row
        if($(this).find(":checkbox").is(":checked")) {
            $(this).show();
        }else{
            $(this).hide();
        }
    });
}

function nomes_oberts() {
    $("#table_llista_projectes_cont tbody>tr").each(function() { //loop over each row
        if($(this).find("td:eq(2)").text() == "Tancat") {
            $(this).find(":checkbox").prop("checked",false);
            $(this).hide();
        }else{
            $(this).show();
        }
    });
}

function nomes_tancats() {
    $("#table_llista_projectes_cont tbody>tr").each(function() { //loop over each row
        if($(this).find("td:eq(2)").text() == "Obert") {
            $(this).find(":checkbox").prop("checked",false);
            $(this).hide();
        }else{
            $(this).show();
        }
    });
}

function mostrar_tots() {
    $("#table_llista_projectes_cont tbody>tr").each(function() {
            $(this).show();
    });
}

function marcar_boton(){

}

// Al seleccionar un responsable se seleccionarán/deseleccionarán todos los proyectos de los que es responsable
$(document).on("change", ".checkbox_responsable",function(){
    if($(this).hasClass("responsable_oberts"))
        projectes_de_responsable(this,"Obert");
    else
        projectes_de_responsable(this,"Tancat");
});