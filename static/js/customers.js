/* $(document).ready(function() {
  // get data from server
  $.ajax({
    url: '/customers/data',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      // initialize DataTable
      console.log(data)
      $('#myTable').DataTable({
        data: data,
        columns: [
          { data: 'customer_name' },
          { data: 'cus_mobile_no' },
          { data: 'customer_address' }
        ]
      });
    },
    error: function(xhr, textStatus, error) {
      console.log(xhr.statusText);
      console.log(textStatus);
      console.log(error);
    }
  });
});
$(document).ready(function() {
    $('#cust_table').DataTable({
        "paging": true,
        "ordering": true,
        "info": true,
        "searching": true,
        "lengthChange": false,
        "pageLength": 10,
        "language": {
            "paginate": {
                "previous": "<i class='fas fa-chevron-left'></i>",
                "next": "<i class='fas fa-chevron-right'></i>"
            }
        }
    });
    /*$('#cust_table input').unbind().bind('keyup', function() {
        table.search(this.value).draw();
    });

    // Add pagination functionality
    $('#cust_table').removeClass('pagination');
    $('#cust_table a').unbind().bind('click', function() {
        table.page($(this).attr('data-page')).draw(false);
        return false;
    });
}); */

$(document).ready(function() {
    var table = $('#customerTable').DataTable({
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

/*
{
                target: 2,
                visible: false,
                searchable: false,
            },
            {
                target: 3,
                visible: false,
            },*/