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
                text: '<span class="glyphicon glyphicon-check" aria-hidden="true" title="Mostrar només els projectes seleccionats.">  Només Seleccionats</span>',
                action: function(){nomes_seleccionats();}
            },{
                text: '<span class="glyphicon glyphicon-plus-sign" aria-hidden="true" title="Mostrar tots els projectes oberts.">  Només Oberts</span>',
                action: function () {nomes_oberts();}
            },{
                text: '<span class="glyphicon glyphicon-minus-sign" aria-hidden="true" title="Mostrar tots els projectes tancats.">  Només Tancats</span>',
                action: function () {nomes_tancats();}
            },{
                text: '<span class="glyphicon glyphicon-asterisk" aria-hidden="true" title="Mostrar tots els projectes.">  Mostrar Tots</span>',
                action: function () {mostrar_tots();}
            },{
                text: '<span class="glyphicon glyphicon-ok" aria-hidden="true" title="Selecciona tots els projectes oberts.">  Seleccionar Oberts</span>',
                action: function () {seleccionar_oberts();}
            },{
                text: '<span class="glyphicon glyphicon-remove" aria-hidden="true" title="Selecciona tots els projectes tancats.">  Seleccionar Tancats</span>',
                action: function () {seleccionar_tancats();}
            },{
                text: '<span class="glyphicon glyphicon-ban-circle" aria-hidden="true" title="Desselecciona tots els projectes.">  Cap</span>',
                action: function () {cap();}
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
                cargar_cookies();
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
                { data:{'Observaciones':'Observaciones'},"render": function(data){

                    if(data['Observaciones']=="Sense observacions.")
                        return '<a class="btn btn-danger observacions" title="'+data['Observaciones']+'"><span class="glyphicon glyphicon-eye-close" aria-hidden="true"></span></a>';
                    else
                        return '<a class="btn btn-success observacions" title="'+data['Observaciones']+'"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>';
                }},
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
                            if(column==5)// solo nos interesa formatear los numeros de saldo(columna 4)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            else if(column==4)
                                data=$(data).attr("title");
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
                { type: 'num-fmt', targets: [1,2,5] },
                {"width": "10%","className":"dt-center", targets: [0,1,2,4] },
                {"width": "20%", targets:[5]},
                {"width": "40%","className":"dt-left", targets:[3]}
            ],
            drawCallback: function(){
                $(".observacions").tooltip();
            },
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
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
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
                scrollY:        '90vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                columnDefs: [
    //                { type: 'de_date', targets: 0 },
                    {"width": "5%","className":"dt-center", targets: [3] },
                    {"width": "30%","className":"dt-left", targets:[0]},
                    {"width": "20%", type: 'num-fmt', targets: [1,2,4] }

                ],
                columns: [
                    { data:'desc_partida'},
                    { data:'pressupostat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    { data:'gastat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    { data:{'cod':'codigo_entero','id':'id_partida', 'fecha_min':'fecha_min', 'fecha_max':'fecha_max'},"render": function(data){return '<a class="btn btn-info info_compte_pres" id="'+data['id_partida']+'" cod="'+data['codigo_entero']+'"data_min="'+data['fecha_min']+'" data_max="'+data['fecha_max']+'" title="Info" href="#"><span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span></a>';}},
                    { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
                ],
                dom: 'Bfrtip',
                buttons:[{
                    extend: 'print',
                    header: true,
                    footer: true,
                    title: "", //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                    text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                    exportOptions: { columns: '0,1,2,4'},
                    autoPrint: true
                },{
                    extend: 'excel',
                    filename: function(){return "Estat Pressupostari de "+$("#nombre_del_proyecto").text();},
                    text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                    exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                        columns: '0,1,2,4',
                        format: {
                            body: function(data, row, column, node) {
                                if(column==1 || column==2 || column==3)
                                    data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                                return data;
                            }
                        }
                    },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                        var sheet = xlsx.xl.worksheets['sheet1.xml'];
                        $('row c[r^="B"]', sheet).each(function () {// "B" es la columna en el excel
                              $(this).attr('s', 64);
                        });
                        $('row c[r^="C"]', sheet).each(function () {
                              $(this).attr('s', 64);
                        });
                        $('row c[r^="D"]', sheet).each(function () {
                              $(this).attr('s', 64);
                        });
                    }
                },{
                    extend: 'pdf',
                    title: function(){return "Estat Pressupostari de "+$("#nombre_del_proyecto").text();},
                    footer: true,
                    exportOptions: { columns: '0,1,2,4'},
                    text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
                },{
                    extend: 'csv',
                    filename: function(){return "Estat Pressupostari de "+$("#nombre_del_proyecto").text();},
                    footer: true,
                    exportOptions: { columns: '0,1,2,4'},
                    text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
                }],
                footerCallback: function( tfoot, data, start, end, display ) {
                    var api = this.api();
                    $(this).DataTable().columns( [1,2,4] ).every(function(){
    //                    console.log(this.data());
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                        var bgcolor="LightGreen";
                        if(sum<-25)
                            bgcolor="LightCoral";
                        $(this.footer()).attr("bgcolor",bgcolor);
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
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                {"width": "10%", type: 'de_date', targets: 0 },
                {"width": "10%",type: 'num-fmt', targets: [1,2,3,5,6] },
                {"width": "40%","className":"dt-left", targets:[4]}
            ],
            columns: [
                { data:'data' },
                { data:'asiento' },
                { data:'compte' },
                { data:'clau' },
                { data:'descripcio' },
//                { data:'pagat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'despesa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo_disponible', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: "Llista Despeses de "+$("#nombre_del_proyecto").text(), //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return "Llista Despeses de "+$("#nombre_del_proyecto").text();},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    format: {
                        body: function(data, row, column, node) {
                            if( column==5 || column==6)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="F"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="G"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: function(){return "Llista Despeses de "+$("#nombre_del_proyecto").text();},
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return "Llista Despeses de "+$("#nombre_del_proyecto").text();},
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {
                var api = this.api();
                $(this).DataTable().columns( [5,6] ).every(function(index){
//                    console.log(this.data());
                    if(index==5)
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                    else{
                        var sum = this.cell(":last",6).data();
                        if(!sum)
                            sum="0.00";
                    }
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
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
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                {"width": "10%", type: 'de_date', targets: 0 },
                {"width": "10%",type: 'num-fmt', targets: [1,2] },
                {"width": "40%","className":"dt-left", targets:[3]},
                {"width": "10%",type: 'num-fmt', targets: [4,5] }
            ],
            columns: [
                { data: "data" },
                { data: "asiento" },
                { data: "compte" },
                { data: "descripcio" },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){ return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();}, //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    format: {
                        body: function(data, row, column, node) {
                            if(column==4 || column==5)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="F"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,

                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [4,5] ).every(function(index){
//                    console.log(this.data());
                    if(index==5){
                        var sum = this.cell(":last",5).data();
                        if(!sum)
                            sum="0.00";
                    }else
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
                });
            },
            language: opciones_idioma
        });
    }

    if($(".table_fitxa_major_prj")){// INGRESOS I DESPESES (FITXA MAJOR PROJECTES)
       $(".table_fitxa_major_prj").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [6,7] },
                {"width": "5%","className":"dt-center", targets: [0,1,2,5] },
                {"width": "10%", targets:[6,7]},
                {"width": "30%","className":"dt-left", targets:[3,4]}
            ],
            columns: [
                { data:'data'},
                { data:'asiento'},
                { data:'compte'},
                { data:'desc_compte'},
                { data:'descripcio'},
                { data:{'Observaciones':'Observaciones'},"render": function(data){
                    if(data['Observaciones']=="Sense observacions.")
                        return '<a class="btn btn-danger observacions" title="'+data['Observaciones']+'"><span class="glyphicon glyphicon-eye-close" aria-hidden="true"></span></a>';
                    else
                        return '<a class="btn btn-success observacions" title="'+data['Observaciones']+'"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>';
                }},
                { data:'despesa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
//                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){ return "Ingressos i despeses de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();}, //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true,
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==5)
                                data=$(data).attr("title");
                            return data;
                        }
                    }
                }
            },{
                extend: 'excel',
                filename: function(){return "Ingressos i despeses de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==6 || column==7)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            else if(column==5)
                                data=$(data).attr("title");
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
//                    $('row c[r^="E"]', sheet).each(function () {
//                          $(this).attr('s', 64);
//                    });
                    $('row c[r^="H"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="I"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: function(){return "Ingressos i despeses de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==5)
                                data=$(data).attr("title");
                            return data;
                        }
                    }
                }
            },{
                extend: 'csv',
                filename: function(){return "Ingressos i despeses de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==5)
                                data=$(data).attr("title");
                            return data;
                        }
                    }
                }
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [6,7] ).every(function(){
//                    console.log(this.data());
                    var sum = this.data().reduce( function (a,b) {
                        return parseFloat(a) + parseFloat(b);
                    },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
                });
            },
            drawCallback: function(){
                $(".observacions").tooltip();
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
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                { type: 'num-fmt', targets: [2,3,4,5,6,7,8] },
                { type: 'text', targets: [1] },
                {"width": "5%","className":"dt-center", "targets": [0,3] },
                {"width": "10%","className":"dt-center", "targets": [1,2,4,5,6,7,8] }
            ],
            columns: [
                {data:'codi'},
                {data:'nom'},
                { data:'concedit', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                //{ data:'iva', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_total', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingressos', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'pendent', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'despeses', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                //{ data:'disponiblecaixa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'disponible_real', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: function(){ return "Estat projectes de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();}, //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return "Estat projectes de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: ':visible',
                    format: {
                        body: function(data, row, column, node) {
                            if(column!=0 && column!=1)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="D"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="F"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="G"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="H"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="I"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
//                    $('row c[r^="J"]', sheet).each(function () {
//                          $(this).attr('s', 64);
//                    });
//                    $('row c[r^="K"]', sheet).each(function () {
//                          $(this).attr('s', 64);
//                    });
                }
            },{
                extend: 'pdf',
                title: function(){return "Estat projectes de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return "Estat projectes de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [2,3,4,5,6,7,8] ).every(function(){
//                    console.log(this.data());
                    var sum = this.data().reduce( function (a,b) {
                        return parseFloat(a) + parseFloat(b);
                    },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
                });

//                $( api.columns( [2,3,4,5,6,7,8] ).footer() ).children("b").each(function(){
//                    $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
//                });
//                var bgcolor="LightGreen";  #OJO! descomentar cuando esta table se adapte a ajax
//                if(sum<-25)
//                    bgcolor="LightCoral";
//                $(this.footer()).attr("bgcolor",bgcolor);
//                $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
            },
            language: opciones_idioma
        });
    }

    if($(".table_resum_fitxa_major_prj")){// RESUM PER PARTIDES(RESUM FITXA MAJOR PROJECTES PER COMPTES)
       $(".table_resum_fitxa_major_prj").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                { type: 'de_date', targets: 0 },
                { type: 'num-fmt', targets: [2,3,5] }
            ],
            columns: [
                { data:'compte'},
                { data:'descripcio'},
                { data:'despesa', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingres', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:{'codigo_entero':'codigo_entero','compte':'compte','fecha_min':'fecha_min', 'fecha_max':'fecha_max'},"render": function(data){return '<a class="btn btn-info info_compte" id="'+data["compte"]+'-'+data["codigo_entero"]+'" data_min="'+data['fecha_min']+'" data_max="'+data['fecha_max']+'" title="Info" href="#"><span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span></a>';}},
                { data:'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                exportOptions: { columns: '0,1,2,3,5'},
                title: function(){ return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();}, //function(dt, node, config){return '<h4>'+$($.fn.dataTable).node().prev("h3").html()+'</h4>'},
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    columns: '0,1,2,3,5',
                    format: {
                        body: function(data, row, column, node) {
                            if(column==2 || column==3 || column==4)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="D"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                exportOptions: { columns: '0,1,2,3,5'},
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: function(){return "Partides de "+$(".ui-accordion-content-active").find(".nombre_del_responsable").html();},
                footer: true,
                exportOptions: { columns: '0,1,2,3,5'},
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [2,3,5] ).every(function(index){
//                    console.log(this.data());
                    if(index==5){
                        var sum = this.cell(":last",5).data();
                        if(!sum)
                            sum="0.00";
                    }else
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
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
                { type: 'num-fmt', targets: [0,1,2,3,4,5,6,7,8,9,10] }
            ],
            columns: [
//                null,
//                null,
                { data:'codi' },
                { data:'responsable' },
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
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: "Resum estat projectes",
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: "Resum estat projectes",
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    format: {
                        body: function(data, row, column, node) {
                            if(column==2 || column==3 || column==4 || column==5 || column==6 || column==7 || column==8 || column==9 || column==10 )
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="D"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="F"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="G"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="H"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="I"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="J"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="K"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: "Resum estat projectes",
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: "Resum estat projectes",
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [2,3,4,5,6,7,8,9,10] ).every(function(){
//                    console.log(this.data());
                    var sum = this.data().reduce( function (a,b) {
                        return parseFloat(a) + parseFloat(b);
                    },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
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
            ajax:{
                url:'/json_vacio/',
                contentType: "application/json;",
                dataSrc: ''
            },
            columnDefs: [
                { type: 'num-fmt', targets: [2,3,4,5,6,7,8,9,10,11,12] }
            ],
            columns: [
                { data:"codi" },
                { data:"nom" },
                { data:'base_canon', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen_1', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_creaf', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen_2', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_oficial', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'dif_canon', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'ingressos', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'percen_3', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'canon_pendent_aplicar', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                { data:'saldo_canon_oficial', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
            ],
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: "Resum estat projectes",
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: "Resum estat projectes",
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    format: {
                        body: function(data, row, column, node) {
                            if(column==2 || column==3 || column==4 || column==5 || column==6 || column==7 || column==8 || column==9 || column==10 )
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="D"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="F"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="G"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="H"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="I"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="J"]', sheet).each(function () {// "B" es la columna en el excel
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="K"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: "Resum estat projectes",
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: "Resum estat projectes",
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [2,4,6,7,8,10,11,12] ).every(function(){
//                    console.log(this.data());
                    var sum = this.data().reduce( function (a,b) {
                        return parseFloat(a) + parseFloat(b);
                    },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
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
            dom: 'Bfrtip',
            buttons:[{
                extend: 'print',
                header: true,
                footer: true,
                title: "Comptes no assignats a cap projecte",
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                autoPrint: true
            },{
                extend: 'excel',
                filename: "Comptes no assignats a cap projecte",
                text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                    format: {
                        body: function(data, row, column, node) {
                            if(column==2 || column==3 || column==4)
                                data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                            return data;
                        }
                    }
                },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="C"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="D"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                    $('row c[r^="E"]', sheet).each(function () {
                          $(this).attr('s', 64);
                    });
                }
            },{
                extend: 'pdf',
                title: "Comptes no assignats a cap projecte",
                footer: true,
                text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
            },{
                extend: 'csv',
                filename: "Comptes no assignats a cap projecte",
                footer: true,
                text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
            }],
            footerCallback: function( tfoot, data, start, end, display ) {// aplicar el formateo en los footers indicados
                var api = this.api();
                $(this).DataTable().columns( [2,3,4] ).every(function(index){
//                    console.log(this.data());
                    if(index==4){
                        var sum = this.cell(":last",4).data();
                        if(!sum)
                            sum="0.00";
                    }else
                        var sum = this.data().reduce( function (a,b) {
                            return parseFloat(a) + parseFloat(b);
                        },0 ); //OJO cambiar a 2????
                    var bgcolor="LightGreen";
                    if(sum<-25)
                        bgcolor="LightCoral";
                    $(this.footer()).attr("bgcolor",bgcolor);
                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
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

    // RESUM ESTAT PROJECTES PER RESPONSABLE
    if($(elemento).find(".table_resum_estat_prj_resp")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_resum_estat_prj_resp").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/show_estat_prj_resp_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("proyectos")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

    // ESTAT PRESSUPOSTARI
    if($(elemento).find(".table_fitxa_major_prj")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_fitxa_major_prj").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/show_fitxa_major_prj_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

    // RESUM PER PARTIDES(RESUM FITXA MAJOR PROJECTES PER COMPTES)
    if($(elemento).find(".table_resum_fitxa_major_prj")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_resum_fitxa_major_prj").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/show_resum_fitxa_major_prj_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

    // RESUM ESTAT CANON PER RESPONSABLES
    if($(elemento).find(".table_resum_estat_canon")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_resum_estat_canon").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/show_resum_estat_canon_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

    // LLISTA DE DESPESES
    if($(elemento).find(".table_llista_despeses")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_llista_despeses").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/cont_despeses_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

    // LLISTA DE INGRESSOS
    if($(elemento).find(".table_llista_ingressos")){ /// no hace falta quitar el each ya que nos sirve para el this o por si alguna vez se añaden mas tablas como esta(poco probable)
        $(elemento).find(".table_llista_ingressos").each(function(){
            var tabla=$(this).DataTable();
            var mensaje=$(this).find(".dataTables_empty");
            mensaje.html("Carregant...");
            tabla.ajax.url('/cont_ingresos_datos/'+$(this).attr("fecha_min")+'/'+$(this).attr("fecha_max")+'/'+$(this).attr("cod")).load();
            tabla.ajax.reload(function(){mensaje.html("No s'han trobat dades");});
        });
    }

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

function seleccionar_oberts() {
    $("#table_llista_projectes_cont tbody>tr").each(function() {
        if($(this).find("td:eq(2)").text() == "Obert") {
            $(this).find(":checkbox").prop("checked",true);
        }else{
            $(this).find(":checkbox").prop("checked",false);
        }
    });
}

function seleccionar_tancats() {
    $("#table_llista_projectes_cont tbody>tr").each(function() {
        if($(this).find("td:eq(2)").text() == "Tancat") {
            $(this).find(":checkbox").prop("checked",true);
        }else{
            $(this).find(":checkbox").prop("checked",false);
        }
    });
}

function cap() {
    $("#table_llista_projectes_cont tbody>tr").each(function() {
        $(this).find(":checkbox").prop("checked",false);
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