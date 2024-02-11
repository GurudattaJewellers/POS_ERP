$(document).ready(function() {
    $('.edit-box').click(function() {
        var box_id = $(this).data('box-id');
        $.ajax({
            url: '/edit_box/' + box_id,
            type: 'GET',
            success: function(response) {
                response = JSON.parse(response)
                console.log(response)
                $('#box_id').val(response.box_id);
                $('#box_name').val(response.box_name);
                $('#box_metal2').val(response.box_metal);
                $('#box_weight').val(response.box_total_weight);
                $('#updated_date').text(response.box_added_date);
            }
        });
    });

   $('.history').click(function() {
  var box_id = $(this).data('box-id');
  console.log(box_id);

  // Destroy any existing DataTable instances
  var table1 = $('#saleHistoryTable').DataTable();
  var table2 = $('#purchaseHistoryTable').DataTable();
  table1.destroy();
  table2.destroy();

  // Initialize the first table
  $('#saleHistoryTable').DataTable({
    "ajax": {
      "url": "/get_box_sale_history/" + box_id,
      "type": "GET",
      "dataSrc": "",
    },
    "searching": true,
    "ordering": true,
    "info": true,
    "lengthChange": true,
    "columns": [
      { "data": "box_name", "width": "10%" },
      { "data": "item_name", "width": "30%" },
      { "data": "item_weight", "width": "10%" },
      { "data": "item_sale_type", "width": "15%" },
      { "data": "item_sale_12", "width": "10%" },
      { "data": "sale_id", "width": "10%" },
      { "data": "box_updated_date", "width": "15%" },
    ],
    "columnDefs": [
      { "width": "90%", "targets": "_all" }
    ]
  });

  // Initialize the second table
  $('#purchaseHistoryTable').DataTable({
    "ajax": {
      "url": "/get_box_purchase_history/" + box_id,
      "type": "GET",
      "dataSrc": "",
    },
    "searching": true,
    "ordering": true,
    "info": true,
    "lengthChange": true,
    "columns": [
      { "data": "box_name", "width": "10%" },
      { "data": "box_total_weight", "width": "30%" },
      { "data": "box_added_weight", "width": "10%" },
      { "data": "box_existed_weight", "width": "15%" },
      { "data": "item_purchase_12", "width": "10%" },
      { "data": "purchase_id", "width": "10%" },
      { "data": "box_updated_date", "width": "15%" },
    ],
    "columnDefs": [
      { "width": "90%", "targets": "_all" }
    ]
  });

  // Show the modal and activate the first tab
  $('#box-history-modal').modal('show');
  $('#box-sale-history-tab1').tab('show');
});



    $('#add_weight').on('input', function(){
        var total_weight = parseFloat($('#box_weight').val()) + parseFloat($('#add_weight').val())
        $('#total_weight').val(total_weight.toFixed(2))
    });

    $('#total_weight').on('input', function(){
        var add_weight = parseFloat($('#total_weight').val()) - parseFloat($('#box_weight').val())
        $('#add_weight').val(add_weight.toFixed(2))
    });

    $('#EditForm').submit(function(e) {
    e.preventDefault();
    var form = $(this);

    $.ajax({
      type: 'POST',
      url: '/edit_box/'+ $('#box_id').val(),
      data: form.serialize(),
      success: function(data) {
        $('#EditBoxModal').modal('hide');
        $('.toast').toast('show');
        window.location.href = "/boxes";
      },
      error: function(data) {
        alert("Data Not Updated")
        console.log('Error:', data);
      }
    });
  });


});