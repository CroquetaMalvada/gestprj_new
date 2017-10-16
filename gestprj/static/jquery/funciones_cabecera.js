$(document).ready(function(){
    ////////// DATATABLES DE LA OPCION "EDICIO" !!!!!!!!

    $("#table_participants_organismes_edicio").children("table").DataTable({
            ajax: {
                url: '/show_TOrganismes/',
                dataSrc: 'results'
            },
            columns:[
                {'data': 'url'},
                {'data': 'id_organisme'},
                {'data': 'nom_organisme'},
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
});