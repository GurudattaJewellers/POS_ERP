$(document).ready(function() {

    /*$.ajax({
    url: "/get_boxes/",
    type: "GET",
    success: function(data) {

        // append the new options to the select element
        $.each(data, function(index, value) {
            $('#boxes').append('<option value="' + value.box_id + '">' + value.box_name + '</option>');
        });
    },
    error: function(xhr, status, error) {
        console.error("AJAX error: " + status + " - " + error);
    }
    });*/

    if ($('#stone_weight').val() == 0) {
      $('#stone_cost_div').hide();
    } else {
      $('#stone_cost_div').show();
    }

    $('#metal').change(function() {
      var selectedValue = $(this).val();
      if (selectedValue === 'Gold') {
        $('#hsn_sac').val('7113');
        $('#purity_gold_div').show();
        $('#purity_silver_div').hide();
        $('#metal_rate').val($('#metal_gold_rate').val())
        $('#metal_rate').css('background-color', 'gold');
        $('#purity_silver').prop('required', false);
        $('#purity_gold').prop('required', true);
      } else if (selectedValue === 'Silver') {
        $('#hsn_sac').val('7114');
        $('#purity_silver_div').show();
        $('#purity_gold_div').hide();
        $('#metal_rate').val($('#metal_silver_rate').val())
        $('#metal_rate').css('background-color', 'silver');
        $('#purity_gold').prop('required', false);
        $('#purity_silver').prop('required', true);
      } else {
        $('#hsn_sac').val('');
        $('#purity_silver_div').hide();
        $('#purity_gold_div').hide();
        $('#purity_gold').prop('required', false);
        $('#purity_silver').prop('required', false);
      }
    });

    $('#hsn_sac').change(function() {
      var selectedValue = $(this).val();
      if (selectedValue === '7113') {
        $('#metal').val('Gold');
        $('#purity_gold_div').show();
        $('#purity_silver_div').hide();
      } else if (selectedValue === '7114') {
        $('#metal').val('Silver');
        $('#purity_silver_div').show();
        $('#purity_gold_div').hide();
      } else {
        $('#metal').val('');
        $('#purity_silver_div').hide();
        $('#purity_gold_div').hide();
      }
    });

    /*$('#other_input').on('input', function() {
        var inputVal = $(this).val();
        $('select#value_added option').each(function() {
          var value = $(this).val();
          var dataValue = $(this).data('value');
          var newValue = inputVal * dataValue;
          $(this).text(value + ' -> ' + newValue.toFixed(3));
          $(this).val(newValue.toFixed(3));
        });
    });*/

    $('#value_added').change(function() {
      var selectedValue = $(this).val();
      $('#va_gross').text((parseFloat($('#gross_weight').val()) * parseFloat($('#value_added').val())/100).toFixed(3));
      $('#va_net').text((parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100).toFixed(3));
    });


    $('#gross_weight').on('input', function(){
        var value = parseFloat($('#gross_weight').val()) - parseFloat($('#stone_weight').val())
        $('#net_weight').val(value)
    });

    $('#stone_weight').on('input', function(){
        var value = parseFloat($('#gross_weight').val()) - parseFloat($('#stone_weight').val())
        $('#net_weight').val(value)
    });

    $('#net_weight').on('input', function(){
        var value = parseFloat($('#gross_weight').val()) - parseFloat($('#net_weight').val())
        $('#stone_weight').val(value)
    });

    $('#settled_amount').on('input', function(){
        var unsettled_amount = parseFloat($('#total_amount').text()) - parseFloat($('#settled_amount').val())
        $('#unsettled_amount').val(unsettled_amount.toFixed(2))
    });

    $('#unsettled_amount').on('input', function(){
        $('#settled_amount').val(0);
        var settled_amount = parseFloat($('#total_amount').text()) - parseFloat($('#unsettled_amount').val())
        $('#settled_amount').val(settled_amount.toFixed(2))
    });

    $('#discount').on('input', function(){
        if($('#unsettled_amount').val() == 0 ){
            var settled_amount = parseFloat($('#total_amount').text()) - parseFloat($('#discount').val())
            $('#settled_amount').val(settled_amount.toFixed(2))
        }else if($('#unsettled_amount').val() > 0 ){
            var unsettled_amount = parseFloat($('#unsettled_amount').val()) - parseFloat($('#discount').val())
            $('#unsettled_amount').val(unsettled_amount.toFixed(2))
        }
        var unsettled_amount = parseFloat($('#total_amount').text()) - parseFloat($('#settled_amount').val())
        $('#unsettled_amount').val(unsettled_amount.toFixed(2))
    });

    function oldMetal() {
        var weight = $('#old_items_weight').val();
        var touch = parseFloat($('#old_items_touch').val());
        var rate = $('#old_items_rate').val();
        var dust = $('#old_items_dust').val();

        if(rate!=0 || weight !=0){
            if (isNaN(touch) || touch===0) {
                alert("Invalid touch value");
            }}

        var old_quote = ((parseFloat(weight) - parseFloat(dust)) * touch/100) * parseFloat(rate);
        return old_quote.toFixed(2); // round to 2 decimal places
    }

    $('#calculate_grossweight').click(function() {
        $('#settled_amount').val(0);
        $('#unsettled_amount').val(0);
        $('#discount').val(0);
        var cal_weight = (parseFloat($('#gross_weight').val()) + (parseFloat($('#gross_weight').val()) * parseFloat($('#value_added').val())/100) ) - parseFloat($('#stone_weight').val());
        var rate = parseFloat($('#metal_rate').val())
        var rate_gst = rate + (rate * 3/100 )
        var price = (cal_weight * rate) + parseFloat($('#making_charge').val()) + parseFloat($('#stone_cost').val())
        var price_gst = (cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))
        var old = parseFloat(oldMetal());
        var total = price_gst - old;

        var cgst = ((cal_weight * rate) * (1.5/100)) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (1.5/100)))
        var sgst = ((cal_weight * rate) * (1.5/100)) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (1.5/100)))

        var currentDate = new Date();
        $('#net_gross').html('(On Gross Weight)')
        $('#sale_date').text(currentDate.toDateString());
        $('#a_b_gst').text(price.toFixed(2));
        $('#cgst').text(cgst.toFixed(2));
        $('#sgst').text(sgst.toFixed(2));
        $('#new_sale_total').text(price_gst.toFixed(2));
        $('#old_quote').text(old.toFixed(2));

        $('#net_gross_p').val('Gross Weight')
        $('#amount_before_gst').val(price.toFixed(2));
        $('#cgst_p').val(cgst.toFixed(2));
        $('#sgst_p').val(sgst.toFixed(2));
        $('#new_sale_total_p').val(price_gst.toFixed(2));
        $('#old_quote_p').val(old.toFixed(2));
        $('#total_amount_p').val(total.toFixed(2));

        if($('#hsn_sac').val() === '7113'){
              $('#total_amount').html("<span class='badge' style='background-color: gold;color: black; display:inline-block;float:right;'>"+total.toFixed(2)+"</span>");
        }else if($('#hsn_sac').val() === '7114'){
              $('#total_amount').html("<span class='badge' style='background-color: silver;color: black; display:inline-block;float:right;'>"+total.toFixed(2)+"</span>");
        }
        $('#settled_amount').val(total.toFixed(2));
        });

    $('#calculate_netweight').click(function() {
        $('#settled_amount').val(0);
        $('#unsettled_amount').val(0);
        $('#discount').val(0);
        var cal_weight = (parseFloat($('#net_weight').val()) + (parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100) );
        var wastage = (parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100)
        var rate = parseFloat($('#metal_rate').val())
        var rate_gst = rate + (rate * 3/100 )
        var price = (cal_weight * rate) + parseFloat($('#making_charge').val()) + parseFloat($('#stone_cost').val())
        var price_gst = (cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))
        var old = parseFloat(oldMetal());
        var total = price_gst - old;

        var cgst = ((cal_weight * rate) * (1.5/100)) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (1.5/100)))
        var sgst = ((cal_weight * rate) * (1.5/100)) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (1.5/100)))


        var currentDate = new Date();
        $('#net_gross').html('(On Net Weight)')
        $('#sale_date').text(currentDate.toDateString());
        $('#a_b_gst').text(price.toFixed(2));
        $('#cgst').text(cgst.toFixed(2));
        $('#sgst').text(sgst.toFixed(2));
        $('#new_sale_total').text(price_gst.toFixed(2));
        $('#old_quote').text(old.toFixed(2));

        $('#net_gross_p').val('Net Weight')
        $('#amount_before_gst').val(price.toFixed(2));
        $('#cgst_p').val(cgst.toFixed(2));
        $('#sgst_p').val(sgst.toFixed(2));
        $('#new_sale_total_p').val(price_gst.toFixed(2));
        $('#old_quote_p').val(old.toFixed(2));
        $('#total_amount_p').val(total.toFixed(2));

        if($('#hsn_sac').val() === '7113'){
              $('#total_amount').html("<span class='badge' style='background-color: gold;color: black; display:inline-block;float:right;'>"+total.toFixed(2)+"</span>");
        }else if($('#hsn_sac').val() === '7114'){
              $('#total_amount').html("<span class='badge' style='background-color: silver;color: black; display:inline-block;float:right;'>"+total.toFixed(2)+"</span>");
        }
        $('#settled_amount').val(total.toFixed(2));
    });

    $('#reset_button').click(function(){

        $('#sale_date').text();
        $('#a_b_gst').text();
        $('#cgst').text();
        $('#sgst').text();
        $('#total_amount').text();

    });

    $('#salesTable').DataTable().destroy();
    var table = $('#salesTable').DataTable({
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


    $('#generateEstimate').click(function (){

            let displayedSelect = null;
            if ($("#purity_gold_div").css("display") !== "none") {
              displayedSelect = $("#purity_gold");
            } else if ($("#purity_silver_div").css("display") !== "none") {
              displayedSelect = $("#purity_silver");
            }

            // Get the selected option text of the displayed select element

            var data = [];

            if($('#net_gross_p').val() == 'Net Weight'){
            var cal_weight = (parseFloat($('#net_weight').val()) + (parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100) );
            var wastage = (parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100)
            var rate = parseFloat($('#metal_rate').val())
            var rate_gst = rate + (rate * 3/100 )
            var price = (cal_weight * rate) + parseFloat($('#making_charge').val()) + parseFloat($('#stone_cost').val())
            var price_gst = (cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))
            var old = parseFloat(oldMetal());
            var total = price_gst - old;

               data = [    [displayedSelect.find("option:selected").text(), parseFloat($('#gross_weight').val()).toFixed(3)]
            ];

            if ($('#stone_weight').val() != 0) {
                data.push(['Stone Weight (less)', parseFloat($('#stone_weight').val()).toFixed(3)]);
                data.push(['', { text: '', border: [true, true, true, true] }]);
                data.push(['Net Weight', parseFloat($('#net_weight').val()).toFixed(3)]);
            } else {
                data.push(['', { text: '', border: [true, true, true, true] }],);
                data.push(['Net Weight', parseFloat($('#net_weight').val()).toFixed(3)]);
            }

            data.push(['Value Added', (parseFloat($('#net_weight').val()) * parseFloat($('#value_added').val())/100).toFixed(3)]);
            data.push(['', { text: '', border: [true, true, true, true] }]);
            data.push(['Total calc Weight', (parseFloat($('#net_weight').val()) + (parseFloat($('#net_weight').val()) * (parseFloat($('#value_added').val())/100))).toFixed(3)]);
            data.push(['Rate + GST(3%)', '* ( ' + parseFloat($('#metal_rate').val()).toFixed(2) + ' + ' + (parseFloat($('#metal_rate').val()) * 3/100 ).toFixed(2) + ' )']);
            data.push(['', { text: '', border: [true, true, true, true] }]);
            data.push(['New Sale Value', ((cal_weight * rate_gst).toFixed(2)) ]);

            if ($('#making_charge').val() != 0) {
                  var MC = ['MC', parseFloat($('#making_charge').val()).toFixed(2)];
                  data.push(MC);
                }
            if ($('#stone_cost').val() != 0) {
                var stoneCost = ['Stone Cost + GST(3%)', parseFloat($('#stone_cost').val()).toFixed(2) + ' + ' + (parseFloat($('#stone_cost').val()) * (3/100)).toFixed(2) ];
                data.push(stoneCost);
            }

           data.push(
                  ['', { text: '', border: [true, true, true, true] }],
                  ['New Total', (parseFloat(cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))).toFixed(2)]
                );

            } else if($('#net_gross_p').val() == 'Gross Weight'){
            var cal_weight = (parseFloat($('#gross_weight').val()) + (parseFloat($('#gross_weight').val()) * parseFloat($('#value_added').val())/100) ) - parseFloat($('#stone_weight').val());
            var rate = parseFloat($('#metal_rate').val())
            var rate_gst = rate + (rate * 3/100 )
            var price = (cal_weight * rate) + parseFloat($('#making_charge').val()) + parseFloat($('#stone_cost').val())
            var price_gst = (cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))
            var old = parseFloat(oldMetal());
            var total = price_gst - old;

                data = [  [displayedSelect.find("option:selected").text() + ' ' + $('#ornament').find("option:selected").text()  + 'Gross Weight', parseFloat($('#gross_weight').val()).toFixed(3)]
                ];

                if ($('#stone_weight').val() != 0) {
                  var stoneWeightLess = ['Stone Weight (less)', parseFloat($('#stone_weight').val()).toFixed(3)];
                  var netWeight = ['', { text: '', border: [true, true, true, true] }];
                  var totalCalcWeight = ['Net Weight', parseFloat($('#net_weight').val()).toFixed(3)];
                  data.push(stoneWeightLess, netWeight, totalCalcWeight);
                }

                data.push(
                  ['Value Added', (parseFloat($('#gross_weight').val()) * parseFloat($('#value_added').val())/100).toFixed(3)],
                  ['', { text: '', border: [true, true, true, true] }],
                  ['Total calc Weight', (parseFloat($('#net_weight').val()) + (parseFloat($('#gross_weight').val()) * (parseFloat($('#value_added').val())/100))).toFixed(3)],
                  ['Rate + GST(3%)', '* ( ' +parseFloat($('#metal_rate').val()).toFixed(2) + ' + ' + (parseFloat($('#metal_rate').val()) * 3/100 ).toFixed(2) + ' )'],
                  ['', { text: '', border: [true, true, true, true] }],
                  ['New Sale Value', (cal_weight * rate_gst).toFixed(2) ],
                );

                if ($('#making_charge').val() != 0) {
                  var MC = ['MC', parseFloat($('#making_charge').val()).toFixed(2)];
                  data.push(MC);
                }

                if ($('#stone_cost').val() != 0) {
                  var stoneCost = ['Stone Cost + GST(3%)', parseFloat($('#stone_cost').val()).toFixed(2) + ' + ' + (parseFloat($('#stone_cost').val()) * (3/100)).toFixed(2) ];
                  data.push(stoneCost);
                }

                data.push(
                  ['', { text: '', border: [true, true, true, true] }],
                  ['New Total', (parseFloat(cal_weight * rate_gst) + parseFloat($('#making_charge').val()) + (parseFloat($('#stone_cost').val()) + (parseFloat($('#stone_cost').val()) * (3/100)))).toFixed(2)]
                );

            }

            var olddata = [];

            if($('#old_items_weight').val() != 0){

                olddata.push(['Old Items Weight', parseFloat($('#old_items_weight').val()).toFixed(3)]);
                olddata.push(['Dust Less',parseFloat($('#old_items_dust').val()).toFixed(3)]);
                olddata.push(['Old Items Touch',(parseFloat($('#old_items_touch').val()).toFixed(2) + '%')]);
                olddata.push(['Old Items Rate',parseFloat($('#old_items_rate').val()).toFixed(2)]);
                olddata.push(['','']);
                olddata.push(['Old Total Value',(((parseFloat($('#old_items_weight').val()) - parseFloat($('#old_items_dust').val())) * (parseFloat($('#old_items_touch').val())/100)) * parseFloat($('#old_items_rate').val())).toFixed(2)]);

            }

            var totaldata = [['Total Payable Amount',$('#total_amount').text()]];

            // define styles
            var styles = {
              header: {
                bold: true,
                fontSize: 16,
                alignment: 'center',
                margin: [0, 0, 0, 10]
              },
              borderless: {
                margin: [0, 5, 0, 15],
                fontSize: 10,
                table: {
                  widths: ['*', '*'],
                  body: [
                    ['','']
                  ]
                }
              }

            };

            // create a document definition
           var docDefinition = {
              pageSize: 'A5',
              pageOrientation: 'portrait',
              content: [
                { text: $('#metal').find("option:selected").text() + ' Estimate Quote (' + $('#net_gross_p').val() + ')', style: 'header' },
                {
                  table: {
                    style: 'borderless',
                    body: data,
                    layout: 'noBorders'
                  }
                },
                { text: '', style: 'header' }
              ],
              styles: styles
            };

            if (olddata.length > 0) {
              docDefinition.content.push(
                { text: 'Old ' + $('#oldmetal').find("option:selected").text() + ' Estimate Quote', style: 'header' },
                {
                  table: {
                    style: 'borderless',
                    body: olddata,
                    layout: 'noBorders'
                  }
                },
                { text: '', style: 'header' }
              );
            }

            docDefinition.content.push({
                table: {
                    style: 'borderless',
                    body: totaldata,
                    layout: 'noBorders'
                }
              },
                { text: '', style: 'header' }
            );



            // create a PDF document
            var pdfDoc = pdfMake.createPdf(docDefinition);

            // open the PDF document in a new tab
            pdfDoc.open();


            });

});


// create new pdf instance
        /* var pdfDoc = new jsPDF();

        pdfDoc.setPageSize('a6');

        pdfDoc.setFontSize(18);
        pdfDoc.text('Estimate Quote', pdfDoc.internal.pageSize.width / 2, 20, {align: 'center'});

        // define column data
        var data = [
          ['Gross Weight', 'gross weight value'],
          ['Value Added (gms)', 'value added value'],
          ['', ''],
          ['Total calculatable Weight', 'total weight value'],
          ['Stone Less Weight', 'stone weight value'],
          ['Net Weight', 'net weight value'],
          ['', ''],
          ['Rate + GST', 'rate + gst value'],
          ['', ''],
          ['Total', 'total value'],
          ['MC', 'mc value'],
          ['', ''],
          ['Total Amount', 'total amount value']
        ];

        // define table layout
        var columnWidth = pdfDoc.internal.pageSize.width / 2;
        var startY = 50;
        var startX = 10;
        var headerHeight = 10;
        var rowHeight = 8;
        var cellPadding = 2;

        // draw table
        pdfDoc.autoTable({
          startY: startY,
          margin: {left: startX},
          head: [],
          body: data,
          columns: [
            {header: '', dataKey: 0, width: columnWidth - cellPadding, headerHeight: headerHeight, cellPadding: cellPadding},
            {header: '', dataKey: 1, width: columnWidth - cellPadding, headerHeight: headerHeight, cellPadding: cellPadding}
          ],
          columnStyles: {
            0: {fontStyle: 'bold', textColor: [0, 0, 0], fillColor: [255, 255, 255]},
            1: {textColor: [0, 0, 0], fillColor: [255, 255, 255]}
          },
          headStyles: {fillColor: [255, 255, 255]},
          bodyStyles: {fillColor: [255, 255, 255]},
          rowStyles: function(row, rowIndex) {
            if (rowIndex == 0 || rowIndex == 3 || rowIndex == 8 || rowIndex == 11 || rowIndex == 13) {
              return {fontStyle: 'bold', textColor: [0, 0, 0], fillColor: [200, 200, 200]};
            } else {
              return {textColor: [0, 0, 0], fillColor: [255, 255, 255]};
            }
          },
          startY: startY + (rowHeight * data.length) + 10
        });

        // draw small table on the bottom left
        var smallTableData = [
          ['Old Ornaments Purchase', ''],
          ['Old Ornaments Weight', 'old ornaments weight value'],
          ['Dust Less Value', 'dust less value'],
          ['Total Calculatable Weight', 'total calculatable weight value'],
          ['Old Touch Value', 'old touch value'],
          ['Total Amount Receivable', 'total amount receivable value']
        ];

        pdfDoc.autoTable({
          startY: pdfDoc.internal.pageSize.height - 50,
          margin: {left: startX},
          head: [],
          body: smallTableData,
          columns: [
            {header: '', dataKey: 0, width: columnWidth - cellPadding, headerHeight: headerHeight, cellPadding: cellPadding},
            {header: '', dataKey: 1, width: columnWidth - cellPadding, headerHeight: headerHeight, cellPadding: cellPadding}
          ],
          columnStyles: {
            0: {fontStyle: 'bold', textColor: [0, 0, 0], fillColor: [255, 255, 255]},
            1: {textColor: [0, 0, 0], fillColor: [255, 255, 255]}
            },
            headStyles: {fillColor: [255, 255, 255]},
            bodyStyles: {fillColor: [255, 255, 255]},
            rowStyles: function(row, rowIndex) {
            if (rowIndex == 0) {
            return {fontStyle: 'bold', textColor: [0, 0, 0], fillColor: [200, 200, 200]};
            } else {
            return {textColor: [0, 0, 0], fillColor: [255, 255, 255]};
            }
            }
            });

            // add final text to the document
            pdfDoc.text('Thank you for your business!', 10, pdfDoc.internal.pageSize.height - 20);

            // save the pdf document
            pdfDoc.save('estimate-quote.pdf'); */

            // define column data