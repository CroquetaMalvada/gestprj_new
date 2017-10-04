$(document).ready(function(){

    $("#id_data_inici_prj").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false});
    $("#id_data_fi_prj").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });
    $("#id_data_docum_web").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });
    $("#formulario_editar_justificacio_personal").children("[name='data_inici']").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });
    $("#formulario_editar_justificacio_personal").children("[name='data_fi']").datepicker({ dateFormat: 'yy-mm-dd' , TimePicker: false });

//    $(".max2dec").on("change",function(){
//        $(this).val( parseFloat($(this).val()).toFixed(2));
//    });

    ///clicks
     $('.servsub').click(function(e){
        mostrar_categorias()
	 });
	 $("#id_categoria").change(function(e){
        actualizar_categorias();
	 });

     $('#fin').click(function(e){
        habilitar_fecha_fi_prj();
	 });
	 $('#checkbox_docum_web').click(function(e){
        habilitar_fecha_es_docum_web();
	 });

        ///
	 $("#checkbox_coordinat").click(function(){
	     actualizar_prj_coordinat();
	 });

	 $("#coordinat_per_creaf").click(function(){
	     actualizar_prj_coordinat();
	 });

	 $("#coordinat_per_altres").click(function(){
	     actualizar_prj_coordinat();
	 });
        ///



//    //ejecutar una vez al cargar la pagina
//    actualizar_categorias();
    var cat_temp=$("#id_id_categoria").val();//esta variable guarda el valor de la categoria guardada en la bdd ya que la siguiente funcion resetea el valor de este inpu
    cargar_categorias();
    $("#id_id_categoria").val(cat_temp);
    $("#id_categoria").val(cat_temp);

    habilitar_fecha_fi_prj();
    if($("#id_es_docum_web").val()=='S')
      $("#checkbox_docum_web").attr("checked",true);
    actualizar_prj_coordinat();
    habilitar_fecha_es_docum_web();


//

    ///////
    $("#content input:not([type=radio],[type=checkbox]),select,textarea").each(function(){
        $(this).addClass("form-control");
    });
    $("#dialogs input:not([type=radio],[type=checkbox]),select,textarea").each(function(){
        $(this).addClass("form-control");
    });

});

function validar_form(formulario){ // OJO que esta adaptado para las comas decimales pero si se introduce "8.5" se enviara como "85"
    var errores=0;
    var form = formulario;
    form.find(".numero").each(function(){
        var numero=parseFloat($(this).val().replace(separador_miles,'').replace(separador_decimales,'.'))//quitamos los separadores de miles y dejamos que los de decimales sean "."
        if(validar_numero(numero))
            $(this).val(formatnumber( numero, "", ".", 2 ));
        else
            errores++;
    });
    if(errores==0)
        return true;
    else{
        alert("Error amb "+errores+" dels camps numerics.");
        return false;
    }
}
function validar_numero(numero){ //comrpueba que el numero este bien escrito
    if(formatnumber( numero, "", ".", 2 )){
        return true;
        }
    else
        return false;
}
function cargar_categorias(){
    $("#id_categoria").val($("#id_id_categoria").val());
    mostrar_categorias();
}

function mostrar_categorias(){////esconde y muestra categorias segun si es servei o subvencio
        $("#id_categoria option").each(function(){
            $(this).attr("hidden",true);
            if($(this).attr("name")==$("#id_serv_o_subven input:checked").val() || $(this).attr("name")==3) //el 3 es mixto y se aplica a servei como a subvencio
                $(this).removeAttr("hidden");
        });
        $("#id_categoria").val($("#id_categoria option:not([hidden])").first().val());
        actualizar_categorias();
}

function actualizar_categorias(){
        $("#id_id_categoria").val($("#id_categoria").val());
}

function actualizar_prj_coordinat(){
    if($("#checkbox_coordinat").is(":checked")){
        $("#id_id_usuari_extern").attr("disabled",true);
        if($("#coordinat_per_creaf").is(":checked"))
            $("#id_es_coordinat").val(2);
        else if($("#coordinat_per_altres").is(":checked")){
            $("#id_es_coordinat").val(4);
            $("#id_id_usuari_extern").attr("disabled",false);
        }else{
            $("#coordinat_per_creaf").attr("checked",true);
            $("#id_es_coordinat").val(2);
        }
        $("#div_personal").show("slide",{'direction':'up'},1000,function(){
            $.fn.dataTable.tables( {visible: true, api: true} ).columns.adjust();//alinear la tabla de centros part
        });

    }else{
        $("#div_personal").hide("slide",{'direction':'up'},1000);
        $("#id_es_coordinat").val(1);
        $("#id_id_usuari_extern").attr("disabled",true)
    }
}

function habilitar_fecha_fi_prj(){
    if($("#fin").is(":checked")){
        $("#id_data_fi_prj").prop("disabled", false);
    }else{
        $("#id_data_fi_prj").prop("disabled", true);
        $("#id_data_fi_prj").val(null);
    }
}

function habilitar_fecha_es_docum_web(){
    if($("#checkbox_docum_web").is(":checked")){
        $("#id_es_docum_web").val("S");

        $("#id_data_docum_web").prop("disabled", false);
    }else{
        $("#id_es_docum_web").val("N");

        $("#id_data_docum_web").prop("disabled", true);
        $("#id_data_docum_web").val(null);
    }
}


