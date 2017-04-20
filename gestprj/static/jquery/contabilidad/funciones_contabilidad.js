$(window).on('beforeunload', function() {
  loading("Carregant...",true);
});
$(document).ready(function(){
    $(document).find("#loading").dialog("close");
    $("#data_min").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date(1997, 0, 1)});//minDate: (new Date(1997, 1 - 1 , 1)), maxDate: 0
    $("#data_max").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false, changeMonth: true, changeYear: true, yearRange: "1997:c", defaultDate: new Date() });
    //asignarles un valor por defecto
    $("#data_min").datepicker("setDate", new Date(1997, 0, 1));
    $("#data_max").datepicker("setDate", new Date());



//EFECTOS ACCORDION
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content",
        create: function(){
            $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();
        },
        activate: function(){
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust();///IMPORTANTE sirve para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
        }
    });

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


    //Al mostrar la info de un compte en "Resum Fitxa Major Projectes per Comptes"
    $(".table_cont").on( 'click', '.info_compte', function (){
	    id_compte = $(this).attr("id");
	    data_min = $("#data_min").val();
	    data_max = $("#data_max").val();
	    descripcio = $(this).parents(".table_cont").DataTable().row(".selected").data()[1];
	    $("#dialog_llista_comptes").attr("title","DETALL MOVIMENTS COMPTE:"+id_compte+" - "+descripcio);
        table_comptes.ajax.url('/show_Moviments_Compte/'+id_compte+'/'+data_min+'/'+data_max);
	    table_comptes.ajax.reload();
	    mostrar_dialog("dialog_llista_comptes");
	});

//	$("#imprimir_compte").click(function(){
//        var divToPrint=document.getElementById('dialog_llista_comptes');
//        var newWin=window.open('','Print-Window');
//        newWin.document.open();
//        newWin.document.write('<html><body onload="window.print()">'+divToPrint.innerHTML+'</body></html>');
//        newWin.document.close();
//        setTimeout(function(){newWin.close();},10);
//	});
});