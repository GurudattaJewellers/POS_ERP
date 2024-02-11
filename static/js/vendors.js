$(document).ready(function() {
    var table = $('#vendorTable').DataTable({
         /*dom: 'lBfrtip',
         "buttons": [
            {
                extend: 'collection',
                text: 'Export',
                buttons: [
                    'copy',
                    'excel',
                    'csv',
                    'pdf',
                    'print'
                ]
            }
        ],

        buttons: [ {
            extend: 'excelHtml5',
            customize: function( xlsx ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];

                $('row c[r^="C"]', sheet).attr( 's', '2' );
            }
        } ],*/
        "scrollY":        "300px",
        "scrollCollapse": true,
        "paging":         true,
        "searching":      true,
        "ordering":       true,
        "info":           true,
        "columnDefs": [
            { "orderable": false, "targets": [2,3,4,5,6,7,8,9,10,11,12,14] },
            { "visible": false, "targets" : [0,5,7,9,10,11]}
        ],
        "language": {
            "search": "",
            "searchPlaceholder": "Search...",
            "zeroRecords": "No matching records found",
            "infoEmpty": "Showing 0 to 0 of 0 entries",
            "infoFiltered": "(filtered from _MAX_ total records)",
            "paginate": {
                "previous": "<",
                "next": ">"
            }
        }
    });
     $('a.toggle-vis').on('click', function (e) {
        e.preventDefault();

        // Get the column API object
        var column = table.column($(this).attr('data-column'));

        // Toggle the visibility
        column.visible(!column.visible());
    });
});