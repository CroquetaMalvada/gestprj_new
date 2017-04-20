var id_prj = null;
var id_current_perso_creaf=0;
var id_current_partida=0;

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


/////IDIOMA DATATABLES
var opciones_idioma = {
    "decimal":        ",",
    "emptyTable":     "No s'han trobat dades",
    "info":           "Mostrant d'_START_ a _END_ de _TOTAL_ resultats",
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

$(document).ready(function(){

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
                refrescaTabla(14);
    });


});


function actu_import_pres_total(){//////////////// suma los importes de la partida y los muestra en periodicitat pressupost
    var total_perio = 0;
    periodicitat_pressupost.rows().every(function(rowindx){//pone a 0 toda la columna
        periodicitat_pressupost.cell(rowindx,5).data(0);
    });
    pressupost.rows().every(function(rowpress){

            $.get("/show_PeriodicitatPartida/"+pressupost.row(rowpress).data()["id_part"],function(data){
                $.each(data["results"],function(index,obj){///si solo pongo data le paso un objeto en lugar e un array y por lo tanto la function no devuelve indice
//                    console.log(periodicitat_pressupost.cell(index,5).data());
                      if(periodicitat_pressupost.cell(index,5).data()!=undefined){
                          periodicitat_pressupost.cell(index,5).data((periodicitat_pressupost.cell(index,5).data()+parseInt(obj['import_field'])));
                          total_perio = total_perio + parseInt(obj['import_field']);
                          $("#total_periodicitat_pressupost").val(total_perio);
                      }
//                    alert(obj["import_field"]);
                });
            });
    })
//    .promise().done(function(){
//        alert(total_perio);
//
//    });
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
                {'data': 'cost_hora'},
                {'render':function(data,type,row){
                    return(parseInt(row.hores)*parseInt(row.cost_hora));
                }},
                {"render": function(){return '<a class="btn btn-info editar_justificacio_personal" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                {"render": function(){return '<a class="btn btn-danger eliminar_justificacio_personal" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
            ],
            columnDefs:[
                {"visible":false,"targets":0}
            ],
//            success:{
//                $(this)
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
                        {'data': 'import_concedit'},
                        {"render": function(){return '<a class="btn btn-info editar_organisme_fin" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_organisme_fin" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [4,5] }
                    ],
                    fnDrawCallback:function(){
                        var total = $(this).DataTable().column( 3 ).data().sum();
                        $("#total_import_organismes_fin").val(total);
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
                        {'data': 'import_rebut'},
                        {"render": function(){return '<a class="btn btn-info editar_organisme_rec" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_organisme_rec" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [4,5] }
                    ],
                    fnDrawCallback:function(){
                        var total = $(this).DataTable().column( 3 ).data().sum();
                        $("#total_import_organismes_rec").val(total);
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
                        {'data': 'import_field'},
                        {"render": function(){return '<a class="btn btn-info editar_justifInterna" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_justifInterna" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [6,7] }
                    ],
                    fnDrawCallback:function(){
                        var total = $(this).DataTable().column( 5 ).data().sum();
                        $("#total_import_justificacions_internes").val(total);
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==13){ //////////  RENOVACIONS
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
                        {'data': 'import_concedit'},
                        {"render": function(){return 0;}},
                        {"render": function(){return 0;}},
                        {"render": function(){return 0;}},
                        {"render": function(){return '<a class="btn btn-info editar_renovacio" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_renovacio" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1]},
                        { "width": "5%", "targets": [8,9] }
                    ],
                    fnDrawCallback:function(){
                        var tabla = $(this).DataTable();
                        
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
                    },
//                    initComplete: function(settings, json) {
//                      if(renovacions_init==false)
//                        renovacions_init = true;
//                      else
//                        actualizar_canoniva();
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
    }else if(tipo==14){ //////////PRESSUPOST
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
                        {'data': 'import_field'},
                        {"render": function(){return '<a class="btn btn-info editar_pressupost" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_pressupost" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1,2]},
                        { "width": "5%", "targets": [5,6] }
                    ],
                    fnInitComplete:function(){/////// OJO fnInitComplete no se ejecuta al actualizar la tabla,mientras que fnDrawCallBack se ejecuta cada vez que la tabla hace un redraw
                        var total = $(this).DataTable().column( 4 ).data().sum();
                        $("#total_import_pressupost").val(total);

                        if($(this).DataTable().cell(0,1).data()!=undefined){
                            id_current_partida=$(this).DataTable().cell(0,1).data();
                            $($(this).DataTable().row(0).node()).addClass('selected');
                        }

                        refrescaTabla(14);
//                        if($(this).DataTable().row( 0 ).data()["id_partida"])
//                            id_current_partida=$(this).DataTable().row( 0 ).data()["id_part"];
//                            alert(id_current_partida);
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
                        {'data': 'import_field'},
                        {"render": function(){return '<a class="btn btn-info editar_periodicitat_partida" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                        {"render": function(){return '<a class="btn btn-danger eliminar_periodicitat_partida" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0,1,2]},
                        { "width": "5%", "targets": [6,7] }
                    ],
                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
                        var total = $(this).DataTable().column( 5 ).data().sum();
                        $("#total_periodicitat_partida").val(total);
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
                        {'data': 'import_field'},
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
    }
}
//crear funcion para limpiar la tabla de organismos de los centros que ya esten participando(al cargar proyecto)

