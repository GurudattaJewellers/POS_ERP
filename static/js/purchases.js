 $(document).ready(function() {
     $('#purchasesTable').DataTable().destroy();
        var table = $('#purchasesTable').DataTable({
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
            "scrollX": true,
            "sScrollX": "100%",
            "sScrollXInner": "110%",
            "scrollY": "500px",
            "scrollCollapse": true,
            "paging":         true,
            "searching":      true,
            "ordering":       true,
            "info":           true,
            "columnDefs": [
                  { "width": "100px", "targets": 0 },
                //{ "orderable": false, "targets": [2,3,4,5,6,7,8,9,10,11,12,14] },
               // { "visible": false, "targets" : [0,5,7,9,10,11]}
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
            },
            "fixedColumns": {
                "leftColumns": 1
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