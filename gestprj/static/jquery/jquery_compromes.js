$(document).ready(function(){
    compromes = crear_datatable(20);
    compromes_partida = crear_datatable(21);

    $("#table_compromes_partida").find("tbody").on( 'click', 'tr', function () {
                id_current_partida_compromes=$("#table_pressupost").DataTable().row(".selected").data()["id_partida"];
//                $("#nombre_partida").html($("#table_pressupost").DataTable().row(".selected").data()["nom_partida"]);
//                refrescaTabla(14);
    });
    $("#table_compromes").find("tbody").on( 'click', '.observar_compromes', function () {
                refrescaTabla(21);
                mostrar_dialog("compromes_partida");
    });
});