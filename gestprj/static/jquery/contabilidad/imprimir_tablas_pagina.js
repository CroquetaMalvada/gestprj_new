$(document).ready(function(){
    $("#imprimir_llistat_projectes_resp_submit").click(function(e){
        var ids_prjs="";
        table_projectes.rows().every(function(rowidx,tableloop,rowloop){
            if($(table_projectes.row(rowidx,0).node()).find(":checkbox").is(':checked')){
                ids_prjs=ids_prjs+$(table_projectes.row(rowidx,0).node()).find(":checkbox").val()+",";
            }
        });
        //$(this).attr("url","/imprimir_resum_estat_prj_resp/"+data_min+"/"+data_max+"/"+ids_prjs+"/");
        $("#impr_data_min").attr("value",$("#data_min").val());
        $("#impr_data_max").attr("value",$("#data_max").val());
        $("#impr_prjs").attr("value",ids_prjs);
        if(ids_prjs==""){
            alert("Error: No hi ha cap projecte seleccionat.");
        }else{
            $("#imprimir_llistat_projectes_resp").submit();
        }
    });

    if($("#imprimir_pagina").length){
//        var css = '@page { size: landscape; }',
//        head = document.head || document.getElementsByTagName('head')[0],
//        style = document.createElement('style');
//
//        style.type = 'text/css';
//        style.media = 'print';
//
//        if (style.styleSheet){
//          style.styleSheet.cssText = css;
//        } else {
//          style.appendChild(document.createTextNode(css));
//        }
//
//        head.appendChild(style);

        var pagina_actual = $("body").html();
        var contenido_imprimir = $("#imprimir_pagina").clone();
        $("body").empty().html(contenido_imprimir);
        window.print();
        $('body').html(pagina_actual);


        //@page {
        //  size: A4;
        //  margin: 0;
        //}
        //@media print {
        //  html, body {
        //    width: 210mm;
        //    height: 297mm;
        //  }
        //}
    }
});
//
//function PrintElem(elem)
//{
//    var mywindow = window.open('', 'PRINT', 'height=100%,width=100%');
//
//    mywindow.document.write('<html><head><title>' + document.title  + '</title>');
//    mywindow.document.write('</head><body >');
//    mywindow.document.write('<h1>' + document.title  + '</h1>');
//    mywindow.document.write(document.getElementById(elem).innerHTML);
//    mywindow.document.write('</body></html>');
//
//    mywindow.document.close(); // necessary for IE >= 10
//    mywindow.focus(); // necessary for IE >= 10*/
//
//    mywindow.print();
//    mywindow.close();
//
//    return true;
//}