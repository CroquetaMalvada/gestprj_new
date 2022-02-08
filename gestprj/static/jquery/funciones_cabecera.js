//VARIABLES GLOBALES
var justificacions_cabecera;
var Admin=0; // Se pone a 1 en la cabecera cuando se logina con permisos de admin,esto evita que se carguen ajax que el usuario normal no vaya a utilizar

var organismes_cabecera;
var usuaris_creaf_cabecera;
var usuaris_externs_cabecera;
var responsables_cabecera;
var pci_cabecera;
var grups_pci_cabecera;
var organismes_grup_pci;
var permisos_usuaris_consultar;


$(document).ready(function(){
    $("#data_min_pci").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
    $("#data_max_pci").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
    //asignarles un valor por defecto
    $("#data_min_pci").datepicker("setDate", new Date(1997, 0, 1));
    $("#data_max_pci").datepicker("setDate", new Date());
    ////////// DATATABLES DE LA OPCION "EDICIO" !!!!!!!!
    if(Admin==1){

        //////////ORGANISMES
        organismes_cabecera= $("#table_organismes_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_organisme'},
                    {'data': 'nom_organisme'},
                    {"render": function(){return '<a class="btn btn-info editar_organisme_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_organisme_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
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
        /////////////USUARIS CREAF
        usuaris_creaf_cabecera = $("#table_usuaris_creaf_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_usuari'},
                    {'data': 'nom_usuari'},
                    {"render": function(){return '<a class="btn btn-info editar_usuari_creaf_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_usuari_creaf_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                ],
                columnDefs:[
                    {"visible":false,"targets":[0,1]},
                    { "width": "5%", "targets": [3,4] }
                ],
                scrollY:        '50vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });
        /////////////USUARIS EXTERNS
        usuaris_externs_cabecera = $("#table_usuaris_externs_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_usuari_extern'},
                    {'data': 'nom_usuari_extern'},
                    {'data': 'nom_organisme'},
                    {"render": function(){return '<a class="btn btn-info editar_usuari_extern_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_usuari_extern_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
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
        /////////////RESPONSABLES
        responsables_cabecera = $("#table_responsables_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_resp'},
                    {'data': 'codi_resp'},
                    {'data': 'nom'},
                    {"render": function(){return '<a class="btn btn-info editar_responsable_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_responsable_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
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

        ///////////////////////////////////////////////////////

        ///////////// JUSTIFICACIONS
        justificacions_cabecera = $("#table_justificacions_cabecera").children("table").DataTable({
                ajax: {
                    url:'/json_vacio/',
                    contentType: "application/json;",
                    dataSrc: ''
                },
                columns:[
                    {'data': 'data'},
                    {'data': 'codi'},
                    {'data': 'nom'},
                    {'data': 'responsable'},
                    {'data': 'periode'},
                    {'data': 'observacions'}
                ],
                columnDefs: [
                    { type: 'de_date', targets: 0 },
                    {"width": "10%", targets:[0,1]},
                    {"width": "20%","className":"dt-left", targets:[2,3,4,5]}
                ],
                dom: 'Bfrtip',
                buttons:[{
                    extend: 'print',
                    header: true,
                    footer: true,
                    title: function(){return $("#table_justificacions_cabecera").attr("title");},
                    text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                    autoPrint: true
                },{
                    extend: 'excel',
                    filename: function(){return $("#table_justificacions_cabecera").attr("title");},
                    text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>'
                },{
                    extend: 'pdf',
                    title: function(){return $("#table_justificacions_cabecera").attr("title");},
                    footer: true,
                    text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
                },{
                    extend: 'csv',
                    filename: function(){return $("#table_justificacions_cabecera").attr("title");},
                    footer: true,
                    text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
                }],
                scrollY:        '70vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });

        ///////////// INFORME POJECTES PERIODE
        informe_periode_cabecera = $("#table_informe_periode_cabecera").children("table").DataTable({
                ajax: {
                    url:'/json_vacio/',
                    contentType: "application/json;",
                    dataSrc: ''
                },
                columns:[
                    {'data': 'data'},
                    {'data': 'codi'},
                    {'data': 'nom'},
                    {'data': 'responsable'},
                    {'data': 'periode'},
                    {'data': 'observacions'}
                ],
                columnDefs: [
                    { type: 'de_date', targets: 0 },
                    {"width": "10%", targets:[0,1]},
                    {"width": "20%","className":"dt-left", targets:[2,3,4,5]}
                ],
                dom: 'Bfrtip',
                buttons:[{
                    extend: 'print',
                    header: true,
                    footer: true,
                    title: function(){return $("#table_justificacions_cabecera").attr("title");},
                    text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                    autoPrint: true
                },{
                    extend: 'excel',
                    filename: function(){return $("#table_justificacions_cabecera").attr("title");},
                    text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>'
                },{
                    extend: 'pdf',
                    title: function(){return $("#table_justificacions_cabecera").attr("title");},
                    footer: true,
                    text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
                },{
                    extend: 'csv',
                    filename: function(){return $("#table_justificacions_cabecera").attr("title");},
                    footer: true,
                    text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
                }],
                scrollY:        '70vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });

        /////////////PERMISOS USUARIOS CONSULTAR PROYECTOS
        permisos_usuaris_consultar = $("#table_permisos_usuaris_consultar").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_prj_usuaris'},
    //                {'data': 'id'},
                    {'data': 'nom_xarxa'},
                    {'data': {'codi_resp':'codi_resp','codi_prj':'codi_prj'},"render": function(data){return data["codi_resp"]+data["codi_prj"]}},
                    {'data': 'acronim'},
                    {"render": function(){return '<a class="btn btn-info editar_permis_usuari_consultar" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_permis_usuari_consultar" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                ],
                columnDefs:[
                    {"visible":false,"targets":[0]},
                    { "width": "5%", "targets": [5,6] }
                ],
                scrollY:        '70vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });

        ///////////////////////////////////////////////////////


        ///////////////////////////// FORMULARIOS:

        ////// ORGANISMES
        $(document).on( 'click', '.editar_organisme_cabecera', function (){

            var form = $("#formulario_editar_organismes_cabecera");
            $("#formulario_editar_organismes_cabecera").attr("action",organismes_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_organismes_cabecera").attr("method","PUT");
            $.get(organismes_cabecera.row(".selected").data()["url"],function( data ){
                form.children("[name='nom_organisme']").val(data["nom_organisme"]);
                form.children("[name='contacte']").val(data["contacte"]);
                form.children("[name='adreca']").val(data["adreca"]);
                form.children("[name='cp']").val(data["cp"]);
                form.children("[name='poblacio']").val(data["poblacio"]);
                form.children("[name='provincia']").val(data["provincia"]);
                form.children("[name='pais']").val(data["pais"]);
                form.children("[name='tel1']").val(data["tel1"]);
                form.children("[name='tel2']").val(data["tel2"]);
                form.children("[name='fax']").val(data["fax"]);
                form.children("[name='e_mail1']").val(data["e_mail1"]);
                form.children("[name='e_mail2']").val(data["e_mail2"]);
            }).done(function( data ){});

            actualizar_organismes_select();
            mostrar_dialog_cabecera("editar_organismes_cabecera");

        });

        $(document).on( 'click', '.eliminar_organisme_cabecera', function (){
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
                        type: "DELETE",
                        url: organismes_cabecera.row(".selected").data()["url"],
                        success: function(result) {
                             organismes_cabecera.$('tr.selected').hide("highlight",{color:"green"},function(){
                                organismes_cabecera.ajax.reload();
                                actualizar_organismes_select();
                             });
                        }
                    });
                },
                cancel: function(){
                }
            });

        });

        ///CREAR UNO
            $("#editar_organismes_crear_cabecera").click(function(){
            $("#formulario_editar_organismes_cabecera").trigger("reset");
            $("#formulario_editar_organismes_cabecera").attr("action","/gestor_TOrganismes/");
            $("#formulario_editar_organismes_cabecera").attr("method","POST");
            mostrar_dialog_cabecera("editar_organismes_cabecera");
        });

       /// AJAX
        $("#formulario_editar_organismes_cabecera").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
        //                    headers: { 'X-HTTP-Method-Override':  }, //no todos los navegadores aceptan DELETE o PUT,con esto se soluciona
                            data: form.serialize(),
                            success: function(result) {
                                 mostrar_dialog_cabecera("table_organismes_cabecera");
                                 organismes_cabecera.ajax.reload();
                                 actualizar_organismes_select();
                            }

                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });


        /////////////////////////////////////////////

        ////// USUARIS CREAF

        $(document).on( 'click', '.editar_usuari_creaf_cabecera', function (){

            var form = $("#formulario_editar_usuari_creaf_cabecera");
            $("#formulario_editar_usuari_creaf_cabecera").attr("action",usuaris_creaf_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_usuari_creaf_cabecera").attr("method","PUT");

            $.get(usuaris_creaf_cabecera.row(".selected").data()["url"],function( data ){
                form.children("[name='nom_usuari']").val(data["nom_usuari"]);
                form.children("[name='adreca']").val(data["adreca"]);
                form.children("[name='cp']").val(data["cp"]);
                form.children("[name='poblacio']").val(data["poblacio"]);
                form.children("[name='provincia']").val(data["provincia"]);
                form.children("[name='pais']").val(data["pais"]);
                form.children("[name='tel1']").val(data["tel1"]);
                form.children("[name='tel2']").val(data["tel2"]);
                form.children("[name='fax']").val(data["fax"]);
                form.children("[name='e_mail1']").val(data["e_mail1"]);
                form.children("[name='e_mail2']").val(data["e_mail2"]);
                form.children("[name='id_organisme']").val(data["id_organisme"]);
            }).done(function( data ){});

            usuaris_creaf_cabecera.ajax.reload();
            mostrar_dialog_cabecera("editar_usuari_creaf_cabecera");
        });

        $(document).on( 'click', '.eliminar_usuari_creaf_cabecera', function (){

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
                    url: usuaris_creaf_cabecera.row(".selected").data()["url"],
                    type: "DELETE",
                    success: function(result) {
                         usuaris_creaf_cabecera.ajax.reload();
                    }
                 });
                },
                cancel: function(){
                }
            });
        });

        //// CREAR UNO
        $("#editar_personal_creaf_crear_cabecera").click(function(){
            $("#formulario_editar_usuari_creaf_cabecera").trigger("reset");
            $("#formulario_editar_usuari_creaf_cabecera").attr("action","/gestor_UsuariCreaf/");
            $("#formulario_editar_usuari_creaf_cabecera").attr("method","POST");
            mostrar_dialog_cabecera("editar_usuari_creaf_cabecera");
    //	    $("#editar_organismes_participants").attr("method","POST")
        });

        /// AJAX
        $("#formulario_editar_usuari_creaf_cabecera").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
                            data: form.serialize(),
                            success: function(result) {
                                 mostrar_dialog_cabecera("table_usuaris_creaf_cabecera");
                                 usuaris_creaf_cabecera.ajax.reload();
                            }
                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });


        ///////////////////////////////////////////////////
        ///////// USUARIS EXTERNS

        $(document).on( 'click', '.editar_usuari_extern_cabecera', function (){
    //        var load = loading("Carregant...");
            var form = $("#formulario_editar_usuari_extern_cabecera");
            $("#formulario_editar_usuari_extern_cabecera").attr("action",usuaris_externs_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_usuari_extern_cabecera").attr("method","PUT");

            $.get(usuaris_externs_cabecera.row(".selected").data()["url"],function( data ){
                form.children("[name='nom_usuari_extern']").val(data["nom_usuari_extern"]);
                form.children("[name='adreca']").val(data["adreca"]);
                form.children("[name='cp']").val(data["cp"]);
                form.children("[name='poblacio']").val(data["poblacio"]);
                form.children("[name='provincia']").val(data["provincia"]);
                form.children("[name='pais']").val(data["pais"]);
                form.children("[name='tel1']").val(data["tel1"]);
                form.children("[name='tel2']").val(data["tel2"]);
                form.children("[name='fax']").val(data["fax"]);
                form.children("[name='e_mail1']").val(data["e_mail1"]);
                form.children("[name='e_mail2']").val(data["e_mail2"]);
                form.children("[name='id_organisme']").val(data["id_organisme"]);
            }).done(function( data ){});
            usuaris_externs_cabecera.ajax.reload();
            mostrar_dialog_cabecera("editar_usuari_extern_cabecera");

        });

         $(document).on( 'click', '.eliminar_usuari_extern_cabecera', function (){

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
                    url: usuaris_externs_cabecera.row(".selected").data()["url"],
                    type: "DELETE",
                    success: function(result) {
                        actualizar_usuaris_externs_select();
                        usuaris_externs_cabecera.ajax.reload();
                    }
                 });
                },
                cancel: function(){
                }
            });
        });

            //// CREAR UNO
            $("#editar_personal_extern_crear_cabecera").click(function(){
                $("#formulario_editar_usuari_extern_cabecera").trigger("reset");
                $("#formulario_editar_usuari_extern_cabecera").attr("action","/gestor_UsuariExtern/");
                $("#formulario_editar_usuari_extern_cabecera").attr("method","POST");
                mostrar_dialog_cabecera("editar_usuari_extern_cabecera");
        //	    $("#editar_organismes_participants").attr("method","POST")
            });

            /// AJAX
            $("#formulario_editar_usuari_extern_cabecera").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
                            data: form.serialize(),
                            success: function(result) {
                                 mostrar_dialog_cabecera("table_usuaris_externs_cabecera");
                                 usuaris_externs_cabecera.ajax.reload();
                                 actualizar_usuaris_externs_select();
                            }

                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });
        /////////////////////////////////////
        ///////// RESPONSABLES

        $(document).on( 'click', '.editar_responsable_cabecera', function (){
    //        var load = loading("Carregant...");
            var form = $("#formulario_editar_responsables_cabecera");
            $("#formulario_editar_responsables_cabecera").attr("action",responsables_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_responsables_cabecera").attr("method","PUT");

            $.get(responsables_cabecera.row(".selected").data()["url"],function( data ){
                form.children("[name='codi_resp']").val(data["codi_resp"]);
                form.children("[name='id_usuari']").val(data["id_usuari"]);
            }).done(function( data ){});
            responsables_cabecera.ajax.reload();
            mostrar_dialog_cabecera("editar_responsables_cabecera");

        });

         $(document).on( 'click', '.eliminar_responsable_cabecera', function (){

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
                    url: responsables_cabecera.row(".selected").data()["url"],
                    type: "DELETE",
                    success: function(result) {
                        actualizar_responsables_select();
                        responsables_cabecera.ajax.reload();
                    }
                 });
                },
                cancel: function(){
                }
            });
        });

            //// CREAR UNO
            $("#editar_responsables_crear_cabecera").click(function(){
                $("#formulario_editar_responsables_cabecera").trigger("reset");
                $("#formulario_editar_responsables_cabecera").attr("action","/gestor_Responsables/");
                $("#formulario_editar_responsables_cabecera").attr("method","POST");
                mostrar_dialog_cabecera("editar_responsables_cabecera");
        //	    $("#editar_organismes_participants").attr("method","POST")
            });

            /// AJAX
            $("#formulario_editar_responsables_cabecera").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
                            data: form.serialize(),
                            success: function(result) {
                                 mostrar_dialog_cabecera("table_responsables_cabecera");
                                 responsables_cabecera.ajax.reload();
                                 actualizar_responsables_select();
                            }

                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });
        /////////////////////////////////////
        /////////////PCI
        pci_cabecera = $("#table_pci_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio/',
                    dataSrc: ''
                },
                columns:[
                    {'data': 'responsable'},
                    {'data': 'codi'},
                    {'data': 'nom'},
                    {'data': 'cobrat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    {'data': 'despeses', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    {'data': 'canon_aplicat', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) },
                    {'data': 'saldo', render: $.fn.dataTable.render.number( separador_miles, separador_decimales, 2 ) }
                ],
//                columnDefs:[
//                    {"visible":false,"targets":[0,1]}
//                ],

                dom: 'Bfrtip',
                buttons:[{
                    extend: 'print',
                    header: true,
                    footer: true,
                    title: function(){return '<h4>'+$("#table_pci_cabecera").attr("title")+'    ('+$("#id_organisme_pci option:selected").text()+')</h4>'},
                    text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
                    autoPrint: true
                },{
                    extend: 'excel',
                    filename: function(){return $("#table_pci_cabecera").attr("title")},
                    text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
                    exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
                        format: {
                            body: function(data, row, column, node) {
                                if(column==3 || column==4 || column==5 || column==6  )
                                    data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
                                return data;
                            }
                        }
                    },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
                       var sheet = xlsx.xl.worksheets['sheet1.xml'];
                       $('row c[r^="D"]', sheet).each(function () {
                              $(this).attr('s', 64);
                       });
                       $('row c[r^="E"]', sheet).each(function () {
                              $(this).attr('s', 64);
                       });
                       $('row c[r^="F"]', sheet).each(function () {
                              $(this).attr('s', 64);
                       });
                       $('row c[r^="G"]', sheet).each(function () {
                              $(this).attr('s', 64);
                       });
                    }
                },{
                    extend: 'pdf',
                    title: function(){return $("#table_pci_cabecera").attr("title")},
                    text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
                },{
                    extend: 'csv',
                    filename: function(){return $("#table_pci_cabecera").attr("title")},
                    text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
                }],
                order:          [[ 0, "asc" ]],
                scrollY:        '50vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });

        ///////////////////////////////////////////////////////
        /////////////////////////////////////
        /////////////GRUPS PCI
        grups_pci_cabecera = $("#table_grups_pci_cabecera").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_grup'},
                    {'data': 'nom_grup'},
                    {"render": function(){return '<a class="btn btn-info editar_grup_pci_cabecera" title="Editar" href="#"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';}},
                    {"render": function(){return '<a class="btn btn-danger eliminar_grup_pci_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                ],
                columnDefs:[
                    {"visible":false,"targets":[0,1]}
                ],

//                dom: 'Bfrtip',
//                buttons:[{
//                    extend: 'print',
//                    header: true,
//                    footer: true,
//                    title: function(){return '<h4>'+$("#table_pci_cabecera").attr("title")+'    ('+$("#id_organisme_pci option:selected").text()+')</h4>'},
//                    text: '<span class="glyphicon glyphicon-print" aria-hidden="true">  Imprimir</span>',
//                    autoPrint: true
//                },{
//                    extend: 'excel',
//                    filename: function(){return $("#table_pci_cabecera").attr("title")},
//                    text: '<span class="glyphicon glyphicon-equalizer" aria-hidden="true"> Excel</span>',
//                    exportOptions: { // Ojo! todo lo que hay en el exportoptions y en el customize sirve para que el excel importe correctamente el numero(co separador de decimales y millares) y lo interprete como tal
//                        format: {
//                            body: function(data, row, column, node) {
//                                if(column==3 || column==4 || column==5 || column==6  )
//                                    data=parseFloat(data.replace(/\./g,'').replace(separador_decimales,'.'));//quitamos los separadores de miles y dejamos que los de decimales sean "." para ello usamos el "/[caracter]/g sin embargo añadimos un '\' ya que el punto signiica todos los caracteres
//                                return data;
//                            }
//                        }
//                    },customize: function( xlsx ) {//como el numero ha pasado por ej de 1.245,15 a 1245.15 ahora esta funcion se encargara de decirle al excel que lo vuelva a transformar a 1.245,15
//                       var sheet = xlsx.xl.worksheets['sheet1.xml'];
//                       $('row c[r^="D"]', sheet).each(function () {
//                              $(this).attr('s', 64);
//                       });
//                       $('row c[r^="E"]', sheet).each(function () {
//                              $(this).attr('s', 64);
//                       });
//                       $('row c[r^="F"]', sheet).each(function () {
//                              $(this).attr('s', 64);
//                       });
//                       $('row c[r^="G"]', sheet).each(function () {
//                              $(this).attr('s', 64);
//                       });
//                    }
//                },{
//                    extend: 'pdf',
//                    title: function(){return $("#table_pci_cabecera").attr("title")},
//                    text: '<span class="glyphicon glyphicon-list-alt" aria-hidden="true"> PDF</span>'
//                },{
//                    extend: 'csv',
//                    filename: function(){return $("#table_pci_cabecera").attr("title")},
//                    text: '<span class="glyphicon glyphicon-align-left" aria-hidden="true"> CSV</span>'
//                }],
                order:          [[ 0, "asc" ]],
                scrollY:        '80vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });

        organismes_grup_pci = $("#table_editar_organisme_grup_pci").children("table").DataTable({
                ajax: {
                    url: '/json_vacio_results/',
                    dataSrc: ""
                },
                columns:[
                    {'data': 'url'},
                    {'data': 'id_grup'},
                    {'data': 'id_organisme'},
                    {'data': 'nom_organisme'},
                    {"render": function(){return '<a class="btn btn-danger eliminar_organisme_grup_pci_cabecera" title="Eliminar" href="#"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a>';}}
                ],
                columnDefs:[
                    {"visible":false,"targets":[0,1,2]}
                ],
                order:          [[ 0, "asc" ]],
                scrollY:        '80vh',
                scrollCollapse: true,
                paging:         false,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
            });


        ///AL CREAR UN GRUP PCI DESDE CERO
        $("#editar_grups_pci").click(function(){
            $("#formulario_editar_grup_pci").trigger("reset");
            $("#formulario_editar_grup_pci").attr("action","/gestor_GrupsPci/");
            $("#formulario_editar_grup_pci").attr("method","POST");
            mostrar_dialog_cabecera("table_editar_grup_pci_cabecera");
            $("#button_cancelar_formulario_editar_grup_pci").show();
            $("#button_tornar_formulario_editar_grup_pci").hide();
            $("#table_editar_organisme_grup_pci").hide();
        });

       /// AJAX CREAR GRUP PCI
        $("#formulario_editar_grup_pci").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
        //                    headers: { 'X-HTTP-Method-Override':  }, //no todos los navegadores aceptan DELETE o PUT,con esto se soluciona
                            data: form.serialize(),
                            success: function(result) {
                                //mostrar_dialog_cabecera("table_grups_pci_cabecera");
                                grups_pci_cabecera.ajax.reload();
                                actualizar_grups_pci_select();
                                $("#table_editar_organisme_grup_pci").show();
                                $("#id_grup_pci_afegir").val(result["id_grup"]);

                                $("#button_cancelar_formulario_editar_grup_pci").hide();
                                $("#button_tornar_formulario_editar_grup_pci").show();
                            }

                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });

        ///// EDITAR GRUP PCI
        $(document).on( 'click', '.editar_grup_pci_cabecera', function (){
            var form = $("#formulario_editar_grup_pci");
            //alert(grups_pci_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_grup_pci").attr("action",grups_pci_cabecera.row(".selected").data()["url"]);
            $("#formulario_editar_grup_pci").attr("method","PUT");
            $.get(grups_pci_cabecera.row(".selected").data()["url"],function( data ){
                form.children("[name='nom_grup']").val(data["nom_grup"]);
                form.children("[name='descripcio']").val(data["descripcio"]);
                $("#id_grup_pci_afegir").val(data["id_grup"]);
                ////////
                organismes_grup_pci.clear();
                organismes_grup_pci.draw();
                organismes_grup_pci.ajax.url("/llista_organismes_grup_pci/"+$("#id_grup_pci_afegir").val());
                organismes_grup_pci.ajax.reload();
            }).done(function( data ){});

            //actualizar_organismes_select();
            $("#button_cancelar_formulario_editar_grup_pci").hide();
            $("#button_tornar_formulario_editar_grup_pci").show();
            mostrar_dialog_cabecera("table_editar_grup_pci_cabecera");
            actualizar_grups_pci_select();
            $("#table_editar_organisme_grup_pci").show();

        });
        ///////////// ELIMINAR UN GRUP PCI
        $(document).on( 'click', '.eliminar_grup_pci_cabecera', function (){
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
                        type: "DELETE",
                        url: grups_pci_cabecera.row(".selected").data()["url"],
                        success: function(result) {
                             grups_pci_cabecera.$('tr.selected').hide("highlight",{color:"green"},function(){
                                grups_pci_cabecera.ajax.reload();
                                actualizar_grups_pci_select();
                             });
                        }
                    });
                },
                cancel: function(){
                }
            });

        });
        ////////////////////////////ASIGNAR ORGANISMO AL GRUPO PCI
        $("#afegir_organisme_a_grup_pci").click(function(){
            $.ajax({
                    type: "POST",
                    data: {"csrfmiddlewaretoken":$("#token_grup_pci_afegir").children("input").val(),"id_grup":$("#id_grup_pci_afegir").val(),"id_organisme":$("#select_organisme_pci").val()},
                    url: "/afegir_organisme_grup_pci/",
                    success: function(result) {
                        organismes_grup_pci.clear();
                        organismes_grup_pci.draw();
                        organismes_grup_pci.ajax.url("/llista_organismes_grup_pci/"+$("#id_grup_pci_afegir").val());
                        organismes_grup_pci.ajax.reload();
                    }
                });
        });

        ///////////////////////////ELIMINAR UN ORGANISMO DEL GRUP PCI
        $(document).on( 'click', '.eliminar_organisme_grup_pci_cabecera', function (){
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
                        type: "DELETE",
                        url: organismes_grup_pci.row(".selected").data()["url"],
                        success: function(result) {
                             organismes_grup_pci.$('tr.selected').hide("highlight",{color:"green"},function(){
                                organismes_grup_pci.ajax.reload();
                             });
                        }
                    });
                },
                cancel: function(){
                }
            });

        });



        ///////////////////////////////////////////////////////

        ////// PERMISOS USUARIS PROJECTES CONSULTAR
        $(document).on( 'click', '.editar_permis_usuari_consultar', function (){

            var form = $("#formulario_permisos_usuaris_consultar_cabecera");
            $("#formulario_permisos_usuaris_consultar_cabecera").attr("action",permisos_usuaris_consultar.row(".selected").data()["url"]);
            $("#formulario_permisos_usuaris_consultar_cabecera").attr("method","PUT");
            $.get(permisos_usuaris_consultar.row(".selected").data()["url"],function( data ){
                form.children("[name='id_usuari_xarxa']").val(data["id_usuari_xarxa"]);
                form.children("[name='id_projecte']").val(data["id_projecte"]);
            }).done(function( data ){});
            permisos_usuaris_consultar.ajax.reload();
            mostrar_dialog_cabecera("editar_permisos_usuaris_consultar_cabecera");

        });

        $(document).on( 'click', '.eliminar_permis_usuari_consultar', function (){
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
                        type: "DELETE",
                        url: permisos_usuaris_consultar.row(".selected").data()["url"],
                        success: function(result) {
                             permisos_usuaris_consultar.$('tr.selected').hide("highlight",{color:"green"},function(){
                                permisos_usuaris_consultar.ajax.reload();
                             });
                        }
                    });
                },
                cancel: function(){
                }
            });

        });

        ///CREAR UNO
        $("#editar_permisos_usuaris_consultar_crear_cabecera").click(function(){
            $("#formulario_permisos_usuaris_consultar_cabecera").trigger("reset");
            $("#formulario_permisos_usuaris_consultar_cabecera").attr("action","/gestor_PermisosUsuarisConsultar/");
            $("#formulario_permisos_usuaris_consultar_cabecera").attr("method","POST");
            mostrar_dialog_cabecera("editar_permisos_usuaris_consultar_cabecera");
        });

       /// AJAX
        $("#formulario_permisos_usuaris_consultar_cabecera").submit(function(e){
            var form = $(this);
            if(validar_form(form)){
                $.ajax({
                            url: form.attr('action'),
                            type: form.attr('method'),
        //                    headers: { 'X-HTTP-Method-Override':  }, //no todos los navegadores aceptan DELETE o PUT,con esto se soluciona
                            data: form.serialize(),
                            success: function(result) {
                                 mostrar_dialog_cabecera("table_permisos_usuaris_consultar");
                                 permisos_usuaris_consultar.ajax.reload();
                            }

                });
            }
            e.preventDefault(); //para no ejecutar el actual submit del form
        });

        //////////////////////////////

        ////////DIALOGS CABECERA
        $("#dialogs_cabecera").dialog({
            resizable:true,
            modal:true,
            width:"1000px",
            autoOpen:false,
            show: {
                effect: "fade",
                duration: 500
            },
            hide: {
                effect: "fade",
                duration: 500
            }
        });


        $("#dialogs_cabecera").dialog("close");

        ///ACTUALIZAR SELECTS *LAS FUNCIONES ESTAN EN EFECTOS PROJECTE NOU Y TAMBIEN LAS OTRAS 2 LLAMADAS A LAS MISMAS
        if(Admin==1){
            if($("#formulario_nou_projecte").length){
                actualizar_usuaris_xarxa_select();
                actualizar_projectes_select();
                actualizar_responsables_select();
                actualizar_usuaris_creaf_select();
            }
        }

    }

});

function mostrar_dialog_cabecera(dialog){
//    var titulo = "";
    $("#dialogs_cabecera").dialog("open");
    $(".dialogcabecera").each(function(){
        $(this).hide();
        if($(this).attr("id")==dialog){
             $(this).show();
    //         titulo = $(this).attr("title");
             $("#dialogs_cabecera").dialog({"title":$(this).attr("title")});
        }
    });
    $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();

}

function dialog_justificacions_cabecera(){
    return $.confirm({
            title:"Justificacions",
            content:'Data inici:  <input id="data_min_justificacions_cabecera" /><br>Data final: <input id="data_max_justificacions_cabecera" />',
            onOpen: function(){
                $("#data_min_justificacions_cabecera").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
                $("#data_max_justificacions_cabecera").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
                //asignarles un valor por defecto
                $("#data_min_justificacions_cabecera").datepicker("setDate", new Date(1997, 0, 1));
                $("#data_max_justificacions_cabecera").datepicker("setDate", new Date());
            },
            confirmButton: 'Buscar',
            cancelButton: 'Cancel·lar',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            confirm: function(){
//                var tabla=$("#table_justificacions_cabecera").children("table").DataTable()
                justificacions_cabecera.ajax.url("/llista_justificacions_cabecera/"+$("#data_min_justificacions_cabecera").val()+"/"+$("#data_max_justificacions_cabecera").val()).load();
                justificacions_cabecera.ajax.reload();
                $("#table_justificacions_cabecera").attr("title","Justificacions de projectes de "+$("#data_min_justificacions_cabecera").val()+" a "+$("#data_max_justificacions_cabecera").val());
                mostrar_dialog_cabecera("table_justificacions_cabecera");

            }
    });
}

///// DIALOG CABECERA "CONSULTES > PROJECTES PER RESPONSABLE"

function dialog_projectes_per_responsable_cabecera(){
    $.ajax({
                url: '/llista_projectes_responsable_consultar/',
    //                    type: form.attr('method'),
    //                    data: form.serialize(),
                datatype:'json',
                success: function(result) {
                    var html="";
                    var titulo="<button onclick='imprimir_projectes_resp_cabecera();' class='btn btn-info'><span class='glyphicon glyphicon-print' aria-hidden='true'></span> Imprimir resultats</button>";
//                    html=html+'<a onclick="imprimir_projectes_resp_cabecera();" class="glyphicon glyphicon-print" aria-hidden="true">Imprimir</a>'
                    html="<div id='contenido_projectes_responsable_consultar'><h2>PROJECTES PER RESPONSABLE ( "+$.datepicker.formatDate('dd/mm/yy', new Date())+" )</h2>"
                    $(result).each(function(){
                        html=html+"<h3>"+this.codi_investigador+" - "+this.nom_responsable+"</h3><table class='table table-striped table-bordered tabla_projectes_resp_consultar'><thead><tr><th>Codi</th><th>Nom</th><th>Entitat Finançadora</th></tr></thead>";
                        $(this.projectes).each(function(){
                            html=html+"<tr><td>"+this.codi+"</td><td>"+this.nom+"</td><td>"+this.entitats+"</td></tr>"
                        });
                        html=html+"</table><br>";
                    });
                    html=html+"</div>";

                 return $.confirm({
                    title:titulo,
                    content:html,
                    cancelButton: 'Tancar',
                    confirmButton: false,
                    columnClass: 'xlarge',
                    closeIcon: true,
                    onOpen: function(){
                        $(".tabla_projectes_resp_consultar").DataTable({
                            //$(this).DataTable({
                                //scrollY:        '50vh',
                                scrollCollapse: true,
                                paging:         false,
                                autowidth:      true,
                                overflow:       "auto",
                                language: opciones_idioma,
                            //});
                        });

                    }
                 });

                }

    });
}

///// DIALOG CABECERA "CONSULTES > INFORME DE PROJECTES EN PERIODE"
function dialog_informe_projectes_periode(tipo){
    return $.confirm({
            title:"Informe de projectes en període",
            content:'Data inici:  <input id="data_min_informe_periode_cabecera" /><br>Data final: <input id="data_max_informe_periode_cabecera" /><br><h5>Generar en format:</h5><input type="radio" name="tipo_informe" value="1" checked>Xlsx( Excel )</input><br><input type="radio" name="tipo_informe" value="2">Csv</input>',
            onOpen: function(){
                $("#data_min_informe_periode_cabecera").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
                $("#data_max_informe_periode_cabecera").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
                //asignarles un valor por defecto
                $("#data_min_informe_periode_cabecera").datepicker("setDate", new Date(1997, 0, 1));
                $("#data_max_informe_periode_cabecera").datepicker("setDate", new Date());
            },
            confirmButton: 'Generar',
            cancelButton: 'Cancel·lar',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            confirm: function(){
                $("#form_generar_informe_periode_cabecera_data_ini").attr("value",$("#data_min_informe_periode_cabecera").val());
                $("#form_generar_informe_periode_cabecera_data_fin").attr("value",$("#data_max_informe_periode_cabecera").val());
                $("#form_generar_informe_periode_cabecera_tipo").attr("value",$('input[name=tipo_informe]:checked').val());
                //$("#form_generar_informe_periode_cabecera").attr("action", "/generar_informe_periode_cabecera/"+$("#data_min_informe_periode_cabecera").val()+"/"+$("#data_max_informe_periode_cabecera").val());
                if(tipo==1){
                    $("#form_generar_informe_periode_cabecera").attr("action","/generar_informe_periode_cabecera/");
                }else if(tipo==2){
                    $("#form_generar_informe_periode_cabecera").attr("action","/generar_informe_financadors_periode_cabecera/");
                }else if(tipo==3){
                    $("#form_generar_informe_periode_cabecera").attr("action","/generar_informe_receptors_periode_cabecera/");
                }else if(tipo==4){
                    $("#form_generar_informe_periode_cabecera").attr("action","/generar_informe_justificacions_internes_periode_cabecera/");
                }else if(tipo==5){
                    $("#form_generar_informe_periode_cabecera").attr("action","/generar_informe_concessions_periode_cabecera/");
                }

                $("#form_generar_informe_periode_cabecera").submit();
//                var tabla=$("#table_justificacions_cabecera").children("table").DataTable()
//                informe_periode_cabecera.ajax.url("/generar_informe_periode_cabecera/"+$("#data_min_informe_periode_cabecera").val()+"/"+$("#data_max_informe_periode_cabecera").val()).load();
//                informe_periode_cabecera.ajax.reload();
//                $("#table_informe_periode_cabecera").attr("title","Informe de projectes actius durant el període de "+$("#data_min_informe_periode_cabecera").val()+" a "+$("#data_max_informe_periode_cabecera").val());
//                mostrar_dialog_cabecera("table_informe_periode_cabecera");

            }
    });
}

///// DIALOG CABECERA "CONSULTES > PCI" *la declaracion de la tabla mas atras
function dialog_pci_cabecera(){
    actualizar_grups_pci_select();
    mostrar_dialog_cabecera("table_pci_cabecera");
}
function buscar_pci_organisme(){ /// consultes > PCI
    //alert($("#id_organisme_pci").val());
    pci_cabecera.clear();
    pci_cabecera.draw();
    pci_cabecera.ajax.url("/llista_pci_consultar/"+$("#id_grup_pci_select").val()+"/"+$("#data_min_pci").val()+"/"+$("#data_max_pci").val());
    pci_cabecera.ajax.reload();
}
///// DIALOG CABECERA "EDICIO > GRUPS PCI" *la declaracion de la tabla mas atras
function dialog_grups_pci_cabecera(){
    grups_pci_cabecera.clear();
    grups_pci_cabecera.draw();
    grups_pci_cabecera.ajax.url("/llista_grups_pci_consultar/");
    grups_pci_cabecera.ajax.reload();
    actualizar_organismes_select();
    mostrar_dialog_cabecera("table_grups_pci_cabecera");
}


function dialog_organismes_cabecera(){
    organismes_cabecera.clear();
    organismes_cabecera.draw();
    organismes_cabecera.ajax.url("/llista_Organismes/");
    organismes_cabecera.ajax.reload();
    mostrar_dialog_cabecera("table_organismes_cabecera");
}

function dialog_usuaris_creaf_cabecera(){
    usuaris_creaf_cabecera.clear();
    usuaris_creaf_cabecera.draw();
    actualizar_organismes_select();
    usuaris_creaf_cabecera.ajax.url("/llista_Usuaris_creaf/");;
    usuaris_creaf_cabecera.ajax.reload();
    mostrar_dialog_cabecera("table_usuaris_creaf_cabecera");
}

function dialog_usuaris_externs_cabecera(){
    usuaris_externs_cabecera.clear();
    usuaris_externs_cabecera.draw();
    actualizar_organismes_select();
    usuaris_externs_cabecera.ajax.url("/llista_Usuaris_externs/");
    usuaris_externs_cabecera.ajax.reload();
    mostrar_dialog_cabecera("table_usuaris_externs_cabecera");
}

function dialog_responsables_cabecera(){
    responsables_cabecera.clear();
    responsables_cabecera.draw();
    actualizar_usuaris_creaf_select();
    responsables_cabecera.ajax.url("/llista_Responsables/");
    responsables_cabecera.ajax.reload();
    mostrar_dialog_cabecera("table_responsables_cabecera");
}

function dialog_permisos_usuaris_consultar(){
    permisos_usuaris_consultar.clear();
    permisos_usuaris_consultar.draw();
    actualizar_usuaris_xarxa_select();
    actualizar_projectes_select();
    permisos_usuaris_consultar.ajax.url("/llista_permisos_usuaris_consultar/");
    permisos_usuaris_consultar.ajax.reload();
    mostrar_dialog_cabecera("table_permisos_usuaris_consultar");
}

/// IMPRIMIR LOS RESULTADOS DE LA CONSULTA DE PROJECTES PER RESPONSABLE(BOTON GENERADO EN LA FUNCION)
function imprimir_projectes_resp_cabecera(){
    $("#contenido_projectes_responsable_consultar").printArea({"mode":"popup"});
}

function mostrar_permisos_usuaris_consultar(){
    mostrar_dialog_cabecera("table_permisos_usuaris_consultar");
}