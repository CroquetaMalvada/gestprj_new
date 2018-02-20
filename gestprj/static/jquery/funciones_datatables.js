var id_prj = null;
var id_current_perso_creaf=0;
var id_current_partida=0;
var id_current_partida_compromes=0;
var separador_miles='.';
var separador_decimales=',';

var centres_participants = null;
var organismes = null;
var proyectos_user = null;

var personal_creaf = null;
var usuaris_creaf = null;

var personal_extern = null;
var usuaris_externs = null;

var justificacions_personal = null;

var organismes_fin = null;
var organismes_rec = null;

var justificacions_internes = null;

var renovacions = null;
var renovacions_init = false;

var pressupost = null;
var periodicitat_pressupost = null;
var periodicitat_partida = null;
var desglossament = null;

var justificacions_projecte = null;
var auditories = null;
var compromes = null;
var compromes_partida = null;

var separador_decimales = ',';
var separador_miles = '.';


/////IDIOMA DATATABLES
var opciones_idioma = {
    "decimal":        separador_decimales,
    "thousands":      separador_miles,
    "emptyTable":     "No s'han trobat dades",
    "info":           "Mostrant d'_START_ a _END_ de _TOTAL_ resultats",
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

$(document).ready(function(){

//    $(".number").each(function(){
//        $(this).val()=formatnumber( $(this).val(), separador_miles, separador_decimales, 2 );
//    });

    $("#id_id_projecte").attr("value",id_prj);

    if(id_prj!=null)
        centres_participants = crear_datatable(2);
    else
        centres_participants = crear_datatable(1);


    $(".datatable").find("tbody").on( 'click', 'tr', function () {
//        if ( $(this).hasClass('selected') ) {
//            $(this).removeClass('selected');
//        }
//        else {
            $(this).parents("table").find('tr.selected').removeClass('selected');
            $(this).addClass('selected');
//        }
    } );

    $("#table_pressupost").find("tbody").on( 'click', 'tr', function () {
                id_current_partida=$("#table_pressupost").DataTable().row(".selected").data()["id_part"];
                $("#nombre_partida").html($("#table_pressupost").DataTable().row(".selected").data()["nom_partida"]);
                refrescaTabla(14);
                refrescaTabla(15);
    });


});


function actu_import_pres_total(){//////////////// suma los importes de la partida y los muestra en periodicitat pressupost
    var total_perio = 0;
    var total_perio = 0;
    periodicitat_pressupost.rows().every(function(rowindx){//pone a 0 toda la columna
        periodicitat_pressupost.cell(rowindx,5).data(0);
    });
    pressupost.rows().every(function(rowpress){
            $.get("/show_PeriodicitatPartida/"+pressupost.row(rowpress).data()["id_part"],function(data){
                $.each(data["results"],function(index,obj){///si solo pongo data le paso un objeto en lugar e un array y por lo tanto la function no devuelve indice
//                    console.log(periodicitat_pressupost.cell(index,5).data());
                      if(periodicitat_pressupost.cell(index,5).data()!=undefined){
                          var tot=parseFloat(periodicitat_pressupost.cell(index,5).data())+parseFloat(obj['import_field']);
                          periodicitat_pressupost.cell(index,5).data(formatnumber( tot, separador_miles, separador_decimales, 2 ));
                          total_perio = total_perio + parseFloat(obj['import_field']);
                          //una vez actualizado todo ahora simplemente que se sumen las columnas de la tabla
                          //var suma_pres=periodicitat_pressupost.column(5).data().sum();
                          $(periodicitat_pressupost.column(5).footer()).find("#total_import_periodicitat_pressupost").html(formatnumber( total_perio, separador_miles, separador_decimales, 2 ));
                          // $(periodicitat_partida.column(5).footer()).find("#total_import_periodicitat_partida").html(formatnumber( suma_part, separador_miles, separador_decimales, 2 ));
                          //$("#total_periodicitat_pressupost").val(formatnumber( total_perio, separador_miles, separador_decimales, 2 ));
                      }
//                    alert(obj["import_field"]);
                });

            });
    })
}

function refrescaTabla(tabla){
    if(tabla==1)
        centres_participants.ajax.reload();
    else if(tabla==2)
        organismes.ajax.reload();
    else if(tabla==3)
        personal_creaf.ajax.reload();
    else if(tabla==4)
        usuaris_creaf.ajax.reload();
    else if(tabla==5)
        personal_extern.ajax.reload();
    else if(tabla==6)
        usuaris_externs.ajax.reload();
    else if(tabla==7)
        justificacions_personal.ajax.reload();
    else if(tabla==8)
        organismes_fin.ajax.reload();
    else if(tabla==9)
        organismes_rec.ajax.reload();
    else if(tabla==10)
        justificacions_internes.ajax.reload();
    else if(tabla==11)
        renovacions.ajax.reload();
    else if(tabla==12)
        pressupost.ajax.reload();
    else if(tabla==13)
        periodicitat_pressupost.ajax.reload();
    else if(tabla==14){
            periodicitat_partida.ajax.url('/show_PeriodicitatPartida/'+id_current_partida);
            periodicitat_partida.ajax.reload();
            actu_import_pres_total();
    }else if(tabla==15){
        desglossament.ajax.url('/show_Desglossament/'+id_current_partida);
        desglossament.ajax.reload();
    }else if(tabla==16)
        justificacions_projecte.ajax.reload();
    else if(tabla==17)
        auditories.ajax.reload();
    else if(tabla==21){
        compromes_partida.ajax.url('/show_compromes_partida/'+id_current_partida+'/'+id_prj);
        compromes_partida.ajax.reload();
    }

}

function crear_datatable(tipo){
    if(tipo==1){
       return $("#table_centres_participants").DataTable({
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                columnDefs: [
                    { "width": "5%", "targets": 3 }
                ],
                language: opciones_idioma,
        });
    }else if(tipo==2){
        return $("#table_centres_participants").DataTable({//contiene los centros que participan en este projecto(solo deberia ejecutarse al cargar un proyecto)
                ajax: {
                    url: '/show_centresPart/'+id_prj,
                    dataSrc: 'results',
                },
                columns:[
                {'data': 'url'},
                {'data': 'id_organisme'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-danger quitar_organisme_participant" title="Treure organisme" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}},
                ],
                columnDefs:[
                {"visible":false,"targets":[0,1]},
                { "width": "5%", "targets": 3 }
                ],
                scrollY:        '50vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,

        });
    }else if(tipo==3){//organismos(en principio no se muestran los que estan en el proyecto)
        return $("#table_participants_organismes").children("table").DataTable({
            ajax: {
                url: '/show_TOrganismes/'+id_prj,
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_organisme'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-success afegir_a_centres_participants" title="Afegir" href="#"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-info editar_organisme" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_organisme" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
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
    }else if(tipo==4){// MUESTRA LOS PROYECTOS EXISTENTES
        return $("#table_llista_projectes").DataTable({
            scrollY:        '60vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            order:          [[ 1, "asc" ]],
            columnDefs: [
                { "width": "5%", "targets": [0,2,5] },
                { "width": "20%", "targets": 1 },
                { "width": "15%", "targets": 3 },
                { "width": "50%", "targets": 4 }
            ],
            language: opciones_idioma
        });
    }else if(tipo==5){//usuarios internos que participan en el proyecto y su organizacion
        return $("#table_personal_creaf").DataTable({
            ajax: {
                url: '/show_Personal_creaf_prj/'+id_prj,
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_perso_creaf'},
                {'data': 'nom_usuari'},
                {'data': 'es_justificacio',render: function(data){
//                    var txt = 'Sense justificar';
////                    alert(data); OJO QUE SE EJECUTA MAS VECES DE LA CUENTA,ECHAR MAS TARDE UN VISTAZO!!
//                    if(data!=0)
//                        txt = 'Justificades';
                    return '<a class="btn btn-info mostrar_justific_personal" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>Editar justificacions';
                }},
                {"render": function(){return '<a class="btn btn-danger quitar_personal_creaf" title="Treure usuari" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]},
                { "width": "5%", "targets": 4 }
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });
    }else if(tipo==6){//usuarios internos que no participan en el proyecto y su organizacion
        return $("#table_usuaris_creaf").children("table").DataTable({
            ajax: {
                url: '/show_Personal_creaf/'+id_prj,
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_usuari'},
                {'data': 'nom_usuari'},
                {"render": function(){return '<a class="btn btn-success afegir_a_personal_creaf" title="Afegir" href="#"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-info editar_usuari_creaf" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_usuari_creaf" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]},
                { "width": "5%", "targets": [3,4,5] }
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });
    }else if(tipo==7){//usuarios externos que participan en el proyecto y su organizacion
        return $("#table_personal_extern").DataTable({
            ajax: {
                url: '/show_Personal_extern_prj/'+id_prj,
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_perso_ext'},
                {'data': 'nom_usuari_extern'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-danger quitar_personal_extern" title="Treure usuari" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":[0,1]},
                { "width": "5%", "targets": 4 }
            ],
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });
    }else if(tipo==8){//usuarios externos que no participan en el proyecto y su organizacion
        return $("#table_usuaris_externs").children("table").DataTable({
            ajax: {
                url: '/show_Personal_extern/'+id_prj,
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_usuari_extern'},
                {'data': 'nom_usuari_extern'},
                {'data': 'nom_organisme'},
                {"render": function(){return '<a class="btn btn-success afegir_a_personal_extern" title="Afegir" href="#"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-info editar_usuari_extern" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_usuari_extern" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
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
    }else if(tipo==9){// justificaciones de x usuario creaf
        return $("#table_justificacions_personal").children("table").DataTable({
            ajax: {
                url: '/show_justificPersonal/0',
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'data_inici'},
                {'data': 'data_fi'},
                {'data': 'nom_feina'},
                {'data': 'hores'},
                {'data': 'cost_hora',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                {'render':function(data,type,row){
                    var suma = parseFloat(row.hores)*parseFloat(row.cost_hora);
                    //$($(this).DataTable().column( 6 ).footer()).html( "<b>"+formatnumber( suma, separador_miles, separador_decimales, 2 )+"</b>" );
                    return(suma);
                }},
                {"render": function(){return '<a class="btn btn-info editar_justificacio_personal" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_justificacio_personal" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":0}
            ],
//            footerCallback: function( tfoot, data, start, end, display ) {
//                $(this).DataTable().columns( [4,5] ).every(function(){
//                    var sum = this.data().reduce( function (a,b) {
//                        return parseFloat(a) + parseFloat(b);
//                    },2 );
//                    $( this.footer() ).html( "<b>"+formatnumber( sum, separador_miles, separador_decimales, 2 )+"</b>" );
//                });
//            },
            scrollY:        '50vh',
            scrollCollapse: true,
            paging:         false,
            autowidth:      true,
            overflow:       "auto",
            language: opciones_idioma,
        });
    }else if(tipo==10){ //////////TABLAS FINANÇAMENT  //ORGANISME FINANCAMENT
        return $("#table_organismes_fin").DataTable({
                    ajax: {
                        url: '/show_OrganismesFin/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'nom_organisme'},
                        {'data': 'import_concedit',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_organisme_fin" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_organisme_fin" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [4,5] }
                    ],
//                    fnDrawCallback:function(){
//                        var total = $(this).DataTable().column( 3 ).data().sum();
//                        $("#total_import_organismes_fin").val(total);
//                    },
                    footerCallback: function( tfoot, data, start, end, display ) {
                        var total= $(this).DataTable().column( 3 ).data().sum();
                        $($(this).DataTable().column( 3 ).footer()).find("b").html(formatnumber( total, separador_miles, separador_decimales, 2 ));
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==11){ //////////ORGANISME RECEPTOR
        return $("#table_organismes_rec").DataTable({
                    ajax: {
                        url: '/show_OrganismesRec/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'nom_organisme'},
                        {'data': 'import_rebut',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_organisme_rec" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_organisme_rec" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [4,5] }
                    ],
//                    fnDrawCallback:function(){
//                        var total = $(this).DataTable().column( 3 ).data().sum();
//                        $("#total_import_organismes_rec").val(total);
//                    },
                    footerCallback: function( tfoot, data, start, end, display ) {
                        var total= $(this).DataTable().column( 3 ).data().sum();
                        $($(this).DataTable().column( 3 ).footer()).find("b").html(formatnumber( total, separador_miles, separador_decimales, 2 ));
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==12){ //////////JUSTIFICACIONS INTERNES
        return $("#table_justificacions_internes").DataTable({
                    ajax: {
                        url: '/show_justificInternes/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'data_assentament'},
                        {'data': 'id_assentament'},
                        {'data': 'desc_justif'},
                        {'data': 'import_field',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_justifInterna" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_justifInterna" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [6,7] }
                    ],
//                    fnDrawCallback:function(){
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_import_justificacions_internes").val(total);
//                    },
                    footerCallback: function( tfoot, data, start, end, display ) {
                        var total= $(this).DataTable().column( 5 ).data().sum();
                        $($(this).DataTable().column( 5 ).footer()).find("b").html(formatnumber( total, separador_miles, separador_decimales, 2 ));
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==13){ //////////  RENOVACIONS  !Ojo esta tabla es especial ya que sus datos cambian de forma dinamica al,por ejemplo,modificar los valores del iva,canono oficial en los inputs anteriores
        return $("#table_renovacions").DataTable({
                    ajax: {
                        url: '/show_Renovacions/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'data_inici'},
                        {'data': 'data_fi'},
                        {'data': 'import_concedit',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return 0;}},
                        {"render": function(){return 0;}},
                        {"render": function(){return 0;}},
                        {"render": function(){return '<a class="btn btn-info editar_renovacio" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_renovacio" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [8,9] },
                        { "width": "5%", "targets": [4,5,6,7] }
                    ],
                    fnDrawCallback:function(){
                          if($(this).DataTable().rows().count()>0)
                            actualizar_canoniva();
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==14){ //////////PRESSUPOST  !OJO esta y la de abajo es la unica de presupost que no cambia el total de forma dinamica
        return $("#table_pressupost").DataTable({
                    ajax: {
                        url: '/show_Pressupost/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_part'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'nom_partida'},
                        {'data': 'import_field',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_pressupost" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_pressupost" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1,2]},
                        { "width": "5%", "targets": [5,6] },
                        { type: 'num-fmt', targets: [4] }
                    ],
                    fnInitComplete:function(){/////// OJO fnInitComplete no se ejecuta al actualizar la tabla,mientras que fnDrawCallBack se ejecuta cada vez que la tabla hace un redraw
//                        var total = $(this).DataTable().column( 4 ).data().sum();
//                        $("#total_import_pressupost").val(formatnumber( total, separador_miles, separador_decimales, 2 ));

                        if($(this).DataTable().cell(0,1).data()!=undefined){//al cargar el proyecto seleccionamos por defecto la priemra partida
                            id_current_partida=$(this).DataTable().cell(0,1).data();
                            $($(this).DataTable().row(0).node()).addClass('selected');
                            $("#nombre_partida").html($(this).DataTable().cell(0,3).data());
                        }

                        refrescaTabla(14);
                        refrescaTabla(15);
//                        if($(this).DataTable().row( 0 ).data()["id_partida"])
//                            id_current_partida=$(this).DataTable().row( 0 ).data()["id_part"];
//                            alert(id_current_partida);
                    },
                    footerCallback: function( tfoot, data, start, end, display ) {
                        var total= $(this).DataTable().column( 4 ).data().sum();
                        $($(this).DataTable().column( 4 ).footer()).find("b").html(formatnumber( total, separador_miles, separador_decimales, 2 ));
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==15){ //////////PERIODICITAT PRESSUPOST
        return $("#table_periodicitat_pressupost").DataTable({
                    ajax: {
                        url: '/show_PeriodicitatPres/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_perio'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'etiqueta'},
                        {'data': 'data_inicial'},
                        {'data': 'data_final'},////falta la del import
                        {'import':null,"defaultContent":0},
                        {"render": function(){return '<a class="btn btn-info editar_periodicitat_pressupost" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_periodicitat_pressupost" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [6,7] }
                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_pressupost").val(total);
//
//                    },
//                    fnInitComplete:function(){
//                        var total = $(this).DataTable().column( 4 ).data().sum();
//                        $("#total_import_pressupost").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==16){ //////////PERIODICITAT PARTIDA
        return $("#table_periodicitat_partida").DataTable({
                    ajax: {
                        url: '/show_PeriodicitatPartida/'+id_current_partida,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_periodicitat'},
                        {'data': 'id_partida'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'data_inicial_perio'},
                        {'data': 'data_final_perio'},
                        {'data': 'import_field',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_periodicitat_partida" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}}
//                        {"render": function(){return '<a class="btn btn-danger eliminar_periodicitat_partida" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1,2]},
                        { "width": "5%", "targets": [6] }
                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    footerCallback: function( tfoot, data, start, end, display ) {
                        var total= $(this).DataTable().column( 5 ).data().sum();
                        $($(this).DataTable().column( 5 ).footer()).find("b").html(formatnumber( total, separador_miles, separador_decimales, 2 ));
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==17){ //////////DESGLOSSAMENT
        return $("#table_desglossament").DataTable({
                    ajax: {
                        url: '/show_Desglossament/'+id_current_partida,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_partida'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'compte'},
                        {'data': 'clau'},
                        {'data': 'import_field',render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 )},
                        {"render": function(){return '<a class="btn btn-info editar_desglossament" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_desglossament" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [5,6] }
                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==18){ //////////JUSTIFICACIONS PROJECTE
        return $("#table_justificacions_projecte").DataTable({
                    ajax: {
                        url: '/show_JustificacionsProjecte/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'data_justificacio'},
                        {'data': 'data_inici_periode'},
                        {'data': 'data_fi_periode'},
                        {'data': 'comentaris'},
                        {"render": function(){return '<a class="btn btn-info editar_justificacio_projecte" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_justificacio_projecte" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [6,7] }
                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==19){ //////////AUDITORIES
        return $("#table_auditories").DataTable({
                    ajax: {
                        url: '/show_Auditories/'+id_prj,
                        dataSrc: 'results'
                    },
                    columns:[
                        {'data': 'url'},
                        {'data': 'id_projecte'},
//                        {'render': function(data,type,row){
//                            return '<select></select>'
//                        }},'id_organisme'},
                        {'data': 'data_auditoria'},
                        {'data': 'data_inici_periode'},
                        {'data': 'data_fi_periode'},
                        {'data': 'comentaris'},
                        {"render": function(){return '<a class="btn btn-info editar_auditoria" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_auditoria" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [6,7] }
                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==20){ //////////COMPROMÉS
        return $("#table_compromes").DataTable({
                    ajax: {
                        url: '/show_compromes/'+id_prj,
                        contentType: "application/json;",
                        dataSrc: ''
                    },
                    columns:[
                        {'data': 'id_partida'},
                        {'data': 'desc_partida'},
                        {'data': 'pressupostat'},
                        {'data': 'gastat'},
                        {'data': 'compromes'},
                        {'data': 'lliure'},
                        {"render": function(){return '<a class="btn btn-success observar_compromes" title="Detalls" href="#"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0]},
                        { "width": "5%", "targets": [6] }
                    ],
//                    columnDefs:[
//                        { "width": "5%", "targets": [6,7] }
//                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==21){ //////////COMPROMÉS *este es el del dialog
        return $("#table_compromes_partida").DataTable({
                    ajax: {
                        url: '/show_compromes_partida/0/0',
                        contentType: "application/json;",
                        dataSrc: ''
                    },
                    columns:[
                        {'data': 'cuenta'},
                        {'data': 'coste_mes'},
                        {'data': 'data_inici'},
                        {'data': 'data_final'},
                        {'data': 'duracio_total'},
                        {'data': 'duracio_pendent'},
                        {'data': 'compromes'}
                    ],
//                    columnDefs:[
//                        {"visible":false,"targets":[0]},
//                        { "width": "5%", "targets": [6] }
//                    ],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }
}
//crear funcion para limpiar la tabla de organismos de los centros que ya esten participando(al cargar proyecto)

