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
	    $("#dialog_llista_comptes").attr("title","DETALL DE LES DESPESES DE LA PARTIDA: "+partida);
        table_llista_despeses.ajax.url('/show_Despeses_Compte/'+id_compte+'/'+cod+'/'+data_min+'/'+data_max);
	    table_llista_despeses.ajax.reload();
	    mostrar_dialog("dialog_llista_comptes");
	});

	//Al mostrar la info de un compte en "Resum Fitxa Major Projectes per Comptes"
    $(".datatable").on( 'click', '.info_compte', function (){
	    id_compte = $(this).attr("id");
	    data_min = $("#data_min").val();
	    data_max = $("#data_max").val();
	    descripcio = $(this).parents(".datatable").DataTable().row(".selected",0).data()[1]; // Ojo que al pasarlo a ajax devolvera "descripcio"o algo asi en lguar del 1
	    $("#dialog_llista_comptes").attr("title","DETALL MOVIMENTS COMPTE:"+id_compte+" - "+descripcio);
        table_comptes.ajax.url('/show_Moviments_Compte/'+id_compte+'/'+data_min+'/'+data_max);
	    table_comptes.ajax.reload();
	    mostrar_dialog("dialog_llista_comptes");
	});


    $("#formulario_projectes_cont").submit(function(e){// comprueba que haya al menos un proyecto seleccionado
        var num=0;
        var proyectos=[];
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

    $(".observacions").tooltip();

});

function cargar_cookies(){ //se ejecuta cuando termina de cargar las tablas para evitar problemas con checkbox inexistentes
    //Cargar Cookies
    $( "input[name=opcio_cont][value="+Cookies.get('opcion')+"]" ).trigger( "click" );
    $.each(Cookies.getJSON("proyectos"),function(){
//          alert($( "input[name=prj_select][value="+this+"]" ).val());
        $( "input[name=prj_select][value="+this+"]" ).trigger( "click" );
    });
    $("#data_min").val(Cookies.get('fecha_min',));
    $("#data_max").val(Cookies.get('fecha_max',));

}

function borrar_cookies(){
    Cookies.remove("opcion");
    Cookies.remove("proyectos");
    Cookies.remove("data_min");
    Cookies.remove("data_max");
}