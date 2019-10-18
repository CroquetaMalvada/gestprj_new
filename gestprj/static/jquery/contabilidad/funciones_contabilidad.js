//$(window).on('beforeunload', function() {
//  load = loading("Carregant..."); //al final parece que esto no causa problemas de rendimiento
//});

$(document).ready(function(){
//    alert(llista_responsables);
//    load.close();
    $("#data_min").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
    $("#data_max").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
    //asignarles un valor por defecto
    $("#data_min").datepicker("setDate", new Date(1997, 0, 1));
    $("#data_max").datepicker("setDate", new Date());



//EFECTOS ACCORDION
    var primero_creado=0;
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content",
        create: function(event, ui){
            $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
            if (primero_creado==0){ // por defecto,el primer proyecto está abierto por defecto,ergo cargaremos su ajax
                cargar_ajax_prj(ui.panel);
                primero_creado=1;
            }


        },
        activate: function(event,ui){
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust();///IMPORTANTE sirve para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
            if(ui.newHeader.text()!="") ///que se ejecute solo al abrirlo
                cargar_ajax_prj(ui.newPanel); //CARGA LAS DATATABLES DE CONTABILIDAD DEL PROYECTO QUE HAYAMOS ABIERTO
        }
    });
////

/// formatear numeros que aparecen en la parte superior(la funcion de formatnumber esta en datatables_contabilidad.js pero ahora esta en un script que he creado con alguna modificacion
    if($(".datos_contables")){
        $(".datos_contables").each(function(){
                $(this).html(formatnumber( $(this).html(), separador_miles, separador_decimales, 2 ));
//            $(this).html(formatnumber( $(this), separador_miles, separador_decimales, 2 ));
        });
    }
///

    $("input[name=opcio_cont]").on("click",function(){
        if($(this).val()==1)
            $("#formulario_projectes_cont").attr("action","/cont_dades/");
        else if($(this).val()==2)
            $("#formulario_projectes_cont").attr("action","/cont_estat_pres/");
        else if($(this).val()==3)
            $("#formulario_projectes_cont").attr("action","/cont_despeses/");
        else if($(this).val()==4)
            $("#formulario_projectes_cont").attr("action","/cont_ingresos/");
        else if($(this).val()==5)
            $("#formulario_projectes_cont").attr("action","/cont_fitxa_major_prj/");
        else if($(this).val()==6)
            $("#formulario_projectes_cont").attr("action","/cont_estat_prj_resp/");
        else if($(this).val()==7)
            $("#formulario_projectes_cont").attr("action","/cont_resum_fitxa_major_prj/");
        else if($(this).val()==8)
            $("#formulario_projectes_cont").attr("action","/cont_resum_estat_prj/");
        else if($(this).val()==9)
            $("#formulario_projectes_cont").attr("action","/cont_resum_estat_canon/");
        else if($(this).val()==10)
            $("#formulario_projectes_cont").attr("action","/cont_comptes_no_assignats/");
    });


    //Al mostrar la info de un compte en "Estat Pressupostari Projectes"
    $(".datatable").on( 'click', '.info_compte_pres', function (){
	    id_compte = $(this).attr("id");
	    data_min = $(this).attr("data_min");
	    data_max = $(this).attr("data_max");
	    cod=$(this).attr("cod");
	    //console.log($(this).parents(".datatable").DataTable().row(".selected").data()["desc_partida"]);
	    partida = $(this).parents(".datatable").DataTable().row(".selected",0).data()["desc_partida"];
	    $("#dialog_llista_comptes").attr("title","DETALL DE LES DESPESES DE LA PARTIDA '"+partida+"'");
        table_llista_despeses.ajax.url('/show_Despeses_Compte/'+id_compte+'/'+cod+'/'+data_min+'/'+data_max);
	    table_llista_despeses.ajax.reload();
	    mostrar_dialog("dialog_llista_comptes");
	});

	//Al mostrar la info de un compte en "Resum per partides"(Resum Fitxa Major Projectes per Comptes)
    $(".datatable").on( 'click', '.info_compte', function (){
	    id_compte = $(this).attr("id");
	    data_min = $(this).attr("data_min");
	    data_max = $(this).attr("data_max");
	    descripcio = $(this).parents(".datatable").DataTable().row(".selected",0).data()[1]; // Ojo que al pasarlo a ajax devolvera "descripcio"o algo asi en lguar del 1
	    $("#dialog_llista_comptes").attr("title","DETALL MOVIMENTS COMPTE '"+id_compte+"'");//+" - "+descripcio
        table_comptes.ajax.url('/show_Moviments_Compte/'+id_compte+'/'+data_min+'/'+data_max);
	    table_comptes.ajax.reload();
	    mostrar_dialog("dialog_llista_comptes");
	});

	//Al mostrar el comprometido de un proyecto
    $(".datatable").on( 'click', '.info_compromes_prj', function (){
	    id_projecte = $(this).attr("id");
	    codigo_entero = $(this).attr("codigo_entero");
	    descripcio = $(this).parents(".datatable").DataTable().row(".selected",0).data()[1]; // Ojo que al pasarlo a ajax devolvera "descripcio"o algo asi en lguar del 1
	    $("#dialog_llista_compromes").attr("title","DETALL DEL COMPROMÉS '"+descripcio+"'");
//        table_llista_compromes.ajax.url('/show_compromes_projecte/'+id_projecte+"/"+codigo_entero);
//	    table_llista_compromes.ajax.reload();
        $.ajax({
            url: "/show_compromes_projecte/"+id_projecte+"/"+codigo_entero+"/",
            //type: "post",
            //data: "id_projecte="+id_prj,
            success: function(result) {
                 //console.log(result);
                 table_llista_compromes_compte.clear();
                 table_llista_compromes_compte.rows.add(result["compromes_personal"]);
                 table_llista_compromes_compte.draw();

                 table_llista_compromes_albaranes_compte.clear();
                 table_llista_compromes_albaranes_compte.rows.add(result["compromes_albaran"]);
                 table_llista_compromes_albaranes_compte.draw();

                 table_llista_compromes_pedidos_compte.clear();
                 table_llista_compromes_pedidos_compte.rows.add(result["compromes_pedidos"]);
                 table_llista_compromes_pedidos_compte.draw();
            }

        });
	    mostrar_dialog("dialog_llista_compromes_comptes");
	});

	//Al mostrar el comprometido de un proyecto y cuenta
    $(".datatable").on( 'click', '.info_compromes_compte', function (){
	    id_projecte = $(this).attr("id");
	    compte = $(this).attr("compte");
	    codigo = $(this).attr("cod");
	    //descripcio = $(this).parents(".datatable").DataTable().row(".selected",0).data()[1]; // Ojo que al pasarlo a ajax devolvera "descripcio"o algo asi en lguar del 1
	    $("#dialog_llista_compromes_compte").attr("title","COMPROMÉS DEL COMPTE '"+compte+"'");
        $.ajax({
            url: "/show_compromes_llista_comptes/"+id_projecte+"/"+codigo+"/"+compte,
            //type: "post",
            //data: "id_projecte="+id_prj,
            success: function(result) {
                 //console.log(result);
                 table_llista_compromes_compte.clear();
                 table_llista_compromes_compte.rows.add(result["compromes_personal"]);
                 table_llista_compromes_compte.draw();

                 table_llista_compromes_albaranes_compte.clear();
                 table_llista_compromes_albaranes_compte.rows.add(result["compromes_albaran"]);
                 table_llista_compromes_albaranes_compte.draw();

                 table_llista_compromes_pedidos_compte.clear();
                 table_llista_compromes_pedidos_compte.rows.add(result["compromes_pedidos"]);
                 table_llista_compromes_pedidos_compte.draw();
            }

        });
	    mostrar_dialog("dialog_llista_compromes_compte");
	});

	//Al mostrar el comprometido de un proyecto y una lista de cuentas(de una partida)
    $(".datatable").on( 'click', '.info_compromes_llista_comptes', function (){
	    id_projecte = $(this).attr("id");
	    codigo_entero = $(this).attr("codigo_entero");
	    comptes = $(this).attr("comptes");
	    var nom_partida = $(this).parents(".datatable").DataTable().row(".selected",0).data()["desc_partida"]; // Ojo que al pasarlo a ajax devolvera "descripcio"o algo asi en lguar del 1
//	    console.log($(this).parents(".datatable").DataTable().row(".selected",2).data());
	    $("#dialog_llista_compromes_comptes").attr("title","COMPROMÉS DE LA PARTIDA '"+nom_partida+"'");
        $.ajax({
            url: "/show_compromes_llista_comptes/"+id_projecte+"/"+codigo_entero+"/"+comptes,
            //type: "post",
            //data: "id_projecte="+id_prj,
            success: function(result) {
                 //console.log(result);
                 table_llista_compromes_compte.clear();
                 table_llista_compromes_compte.rows.add(result["compromes_personal"]);
                 table_llista_compromes_compte.draw();

                 table_llista_compromes_albaranes_compte.clear();
                 table_llista_compromes_albaranes_compte.rows.add(result["compromes_albaran"]);
                 table_llista_compromes_albaranes_compte.draw();

                 table_llista_compromes_pedidos_compte.clear();
                 table_llista_compromes_pedidos_compte.rows.add(result["compromes_pedidos"]);
                 table_llista_compromes_pedidos_compte.draw();
            }

        });
//        table_llista_compromes_llista_comptes.ajax.url('/show_compromes_llista_comptes/'+id_projecte+'/'+codigo_entero+'/'+comptes);
//	    table_llista_compromes_llista_comptes.ajax.reload();
	    mostrar_dialog("dialog_llista_compromes_comptes");
	});

    //Mostrar las lineas del comprometido de un albaran
    $(".datatable").on( 'click', '.info_compromes_albaranes_compte', function (){
	    id_albaran = $(this).attr("idalb");
	    compte = $(this).attr("compte");
	    descripcio = $(this).attr("desc");
	    $("#dialog_lineas_albaran").attr("title","LÍNIES DE L'ALBARÀ '"+descripcio+"'");
        table_lineas_albaran.ajax.url('/show_lineas_albaran/'+id_albaran+'/');
	    table_lineas_albaran.ajax.reload();
	    mostrar_dialog("dialog_lineas_albaran");
	});

    //Mostrar las lineas del comprometido de un pedido
    $(".datatable").on( 'click', '.info_compromes_pedidos_compte', function (){
	    id_pedido = $(this).attr("idped");
	    compte = $(this).attr("compte");
	    descripcio = $(this).attr("desc");
	    $("#dialog_lineas_pedido").attr("title","LÍNIES DE COMANDA '"+descripcio+"'");
        table_lineas_pedido.ajax.url('/show_lineas_pedido/'+id_pedido+'/');
	    table_lineas_pedido.ajax.reload();
	    mostrar_dialog("dialog_lineas_pedido");
	});

    //Generar pdf de los detalles de un pedido
    $(".datatable").on( 'click', '.generar_detalles_pedido', function (){
	    num_apunte = $(this).attr("numapunte");
        generar_factura(num_apunte);
	});

    $("#formulario_projectes_cont").submit(function(e){// comprueba que haya al menos un proyecto seleccionado
        var num=0;
        var proyectos=[];
        table_projectes.search('').draw();// borramos el input de busqueda para que se incluyan los proyectos que estaban escondidos a causa del mismo
        table_projectes.rows().every(function(rowidx,tableloop,rowloop){
            if($(table_projectes.row(rowidx,0).node()).find(":checkbox").is(':checked')){
                num=1;
                proyectos.push($(table_projectes.row(rowidx,0).node()).find(":checkbox").val());

//                alert(proyectos.push($(table_projectes.row(rowidx,0).node()).find(":checkbox").val()));
//                return false;
            }

        });
        if(num!=0){

            Cookies.set('proyectos',proyectos, { expires: 1 });
//            alert($('input:checked[name=opcio_cont]').val());
            Cookies.set('opcion',$('input:checked[name=opcio_cont]').val()), { expires: 1 };
            Cookies.set('fecha_min',$("#data_min").val(), { expires: 1 });
            Cookies.set('fecha_max',$("#data_max").val(), { expires: 1 });
            return true;
        }else{
            alert("Error: No hi ha cap projecte seleccionat.");
            return false;
        }

    });

});

function cargar_cookies(){ //se ejecuta cuando termina de cargar las tablas para evitar problemas con checkbox inexistentes
    //Cargar Cookies
    $( "input[name=opcio_cont][value="+Cookies.get('opcion')+"]" ).trigger( "click" );
    $.each(Cookies.getJSON("proyectos"),function(){
//          alert($( "input[name=prj_select][value="+this+"]" ).val());
        $( "input[name=prj_select][value="+this+"]" ).trigger( "click" );
    });
    if(Cookies.get("fecha_max")==undefined){
        $("#data_min").datepicker("setDate", new Date(1997, 0, 1));
        $("#data_max").datepicker("setDate", new Date());
    }else{
        $("#data_min").val(Cookies.get('fecha_min'));
        $("#data_max").val(Cookies.get('fecha_max'));
    }


}

function borrar_cookies(){
    Cookies.remove("opcion");
    Cookies.remove("proyectos");
    Cookies.remove("fecha_min");
    Cookies.remove("fecha_max");
}

function generar_factura(id_pedido){
        $.ajax({
            url: "/show_lineas_pedido_detalles/"+num_apunte+"/",
            //type: "post",
            //data: "id_projecte="+id_prj,
            success: function(result) {
                 //console.log(result);
                 generar_pdf_factura(result);
            }

        });
}
function generar_pdf_factura(datos){
    var cabecera_pdf={text:'Factura '+datos["referencia"],style:"titulo"};
    var lineas=[];
    var cabecera_lineas= [
        {
            text:"Proyecto",
            fillColor: '#eeeeee'
        },{
            text:"Descripción",
            fillColor: '#eeeeee'
        },{
            text:"Uds",
            fillColor: '#eeeeee'
        },{
            text:"PVP",
            fillColor: '#eeeeee'
        },{
            text:"%IVA",
            fillColor: '#eeeeee'
        },{
            text:"Total",
            fillColor: '#eeeeee'
        }
    ];
    lineas.push(cabecera_lineas);
    $.each(datos.lineas, function(){
        var lin=[];
        lin.push(this.centrocoste2);
        lin.push(this.desclin);
        lin.push(this.unidades);
        lin.push(this.prcmoneda);
        lin.push(this.poriva);
        lin.push(this.basemoneda);
        lineas.push(lin);
    });
    //console.log(lineas);
    var all_pdf = {
        header:cabecera_pdf,
        content: [
            {
                    columns:[
                        {
                            width: "50%",
                            table: {
                                headerRows: 1,
    //                            widths: [ '*', 'auto', 100, '*' ],
                                //header: 'Proveedor',
                                body: [
                                    [{
                                        text:"Proveedor",
                                        fillColor: '#eeeeee'
                                    }],
                                    [{
                                    text: ""+datos["nompro"]+"\n"+datos["dirpro"]+"\n"+datos["dtopro"]+" "+datos["pobpro"]+"\n"+datos["nomprovi"]+"\nNif: "+datos["nifpro"]+""
                                    }],
                                ]
                            }
                        }
                    ]
            },
            {text:"\n\n\n"},
            {
                table: {
                    headerRows: 1,
                    widths: [ 'auto', 'auto', 'auto', 'auto' ],//widths: [ '20%', '20%', '20%', '20%' ],
                    //header: 'Proveedor',
                    body: [
                        [
                            {
                                text:"S/Nº factura",
                                fillColor: '#eeeeee'
                            },{
                                text:"Fecha",
                                fillColor: '#eeeeee'
                            },{
                                text:"Proveedor",
                                fillColor: '#eeeeee'
                            },{
                                text:"Ref.Interna",
                                fillColor: '#eeeeee'
                            },
                        ],
                        [
                            {
                            text: ""+datos["referencia"]+""
                            },{
                            text: ""+datos["fecha"]+""
                            },
                            {
                            text: ""+datos["codpro"]+""
                            },
                            {
                            text: ""+datos["serie"]+"/"+datos["referencia"]+""
                            }
                        ],
                    ]
                }
            },
            {text:"\n"},
            {
                table: {
                    //headerRows: 1,
                    widths: [ '10%', '50%', '10%', '10%', '10%', '10%' ],
                    //header: 'Proveedor',
                    body:
                            lineas
                            //[ '   38646','   38646', '   38646', '   38646', '   38646', '   38646' ]
                }
            },
            {text:"\n\n\n"},
            {
                table: {
                    widths: [ '50%' ],
                    body:[
                        [{border: [true, true, true, true],text:"Validación:\n\n\n\n\n\n\n\n"}]
                    ]
                }
            },
            {
                table: {
                    headerRows: 1,
                    widths: [ '20%', '20%', '20%', '20%', '20%' ],
                    //header: 'Proveedor',
                    body: [
                        [
                            {
                                text:"Base imponible",
                                fillColor: '#eeeeee'
                            },{
                                text:"IVA",
                                fillColor: '#eeeeee'
                            },{
                                text:"",
                                fillColor: '#eeeeee'
                            },{
                                text:"IRPF ",
                                fillColor: '#eeeeee'
                            },{
                                text:"Total factura",
                                fillColor: '#eeeeee'
                            }
                        ],
                        [
                            {
                            text: ""+datos["base_imponible"]+""
                            },
                            {
                            text: ""+datos["totivamoneda"]+""
                            },
                            {text:""},
                            {
                            text: ""+datos["totirpfmoneda"]+""
                            },
                            {
                            text: ""+datos["totmoneda"]+""
                            }
                        ]
                    ]
                }
            },{
                table: {
                    headerRows: 1,
                    widths: [ '50%', '40%', '10%' ],
                    //header: 'Proveedor',
                    body: [
                        [
                            {
                                colSpan:3,
                                text:"Condiciones de pago",
                                fillColor: '#eeeeee'
                            },
                            "",""
                        ],
                        [
                            {
                            border: [true,false,false,false],
                            text: "Forma de pago:  "+datos["forpag"]+""
                            },
                            {
                            border: [false,false,false,false],
                            text: "Vencimientos: "
                            },
                            {
                            border: [false,false,true,false],
                            text:""
                            }

                        ],[
                            {
                            border: [true,false,false,false],
                            text: "Doc. de pago:  "+datos["docupago"]+""
                            },
                            {
                            border: [false,false,false,false],
                            text: ""
                            },
                            {
                            border: [false,false,true,false],
                            text:""
                            }

                        ],[
                            {
                                colSpan:3,
                                text:datos["obs"]
                            },"",""
                        ]

                    ]
                }
            },
//            {
//                        image: url_image,
//                        width: 200,
//                        height: 100,
//                        style:"titulo"
//
//            },
//            {text:" "},
//            {text: "Dades bàsiques",style:"header"},
//            {text:" "},
//            //{image:url_image,width:250,alignment: 'center'},
//            {
//                columns:[
//                    [
//                        datos_basicos,
//                        'OBSERVACIONS: '+$("#info_observacions").html(),
//                    ]
//                ]
//            },
//            {text:" "},
//            {text: "Mapa",style:"header"},
//            {text:" "},
//            {text:" "},
//            {
//                columns:[
//                    {
//                        width: "*",
//                        text: "Resum localitats"
//                    },{
//                        width: "*",
//                        text: "Mapa"
//                    }
//                ]
//            },
//            {text:" "},
//            {
//                columns:[
//                    {
//                        width: "*",
//                        table: {
////                            headerRows: 1,
////                            widths: [ '*', 'auto', 100, '*' ],
//                            body: [
//                              [ 'Espècie', $("#info_genere").html()+' '+$("#info_especie").html() ],
//                              [ 'Nº UTMs 10km', $("#td_n_utms_10").text()],
//                              [ 'Nº UTMs 1km', $("#td_n_utms_1").text()],
//                              [ 'Nº Citacions puntuals', $("#td_n_citacions").text()],
//                              [ "Nº Masses d'aigua", $("#td_n_masses").text()],
//                              [ { text: 'Localitats Totals:', bold: true }, $("#td_n_localitats_totals").text() ]
//                            ]
//                        }
//                    },{
////                       stack: [/// esto sirve para que se pueda hacer un width con *
////                            {
////                                image: url_mapa,
////                            }
////                       ],
//                        image: url_mapa,
//                        width: 300,
//                        height: 200
//
//                    }
//
//                ]
//            }

        ],
        styles: {
            header: {
            fontSize: 22,
            bold: true
            },
            titulo: {
            italic: true,
            alignment: 'center'
            }
        }
    };

    pdfMake.createPdf(all_pdf).download('Factura_'+datos["referencia"]+'.pdf');

}