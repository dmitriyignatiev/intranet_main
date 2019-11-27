$(document).ready(function() {
    console.log('ready')

    $('#my_form_id').on('submit', function(e) {
        e.preventDefault();
        var req_id = document.getElementsByName('id')[0].innerText;


        var formData = new FormData($(this)[0]);
        var msg_error = 'An error has occured. Please try again later.';
        var msg_timeout = 'The server is not responding';
        var message = '';
        var form = $('#my_form_id');
        $.ajax({

            data: formData,
            async: false,
            // cache: false,
            processData: false,
            contentType: false,
            url: form.attr('action'),
            type: form.attr('method'),

            error: function(xhr, status, error) {
                if (status === "timeout") {
                    alert(msg_timeout);
                } else {
                    alert(msg_error);
                }
            },
            success: function(response) {
                $('#successAlert').text(response.success).show();
                $('#errorAlert').hide();

            },
            timeout: 7000
        });
    });



    $('#re_write').bind('click', function(e) {


        const llc = document.querySelector("#select2-tora_red-container").innerText;
        const req_id = document.getElementsByName('id')[0].innerText;
        const date_request = document.querySelector('input#date_order_C').value;
        const date_loading_plan = document.querySelector('input#date_loading_plan').value;
        const date_unloading_date = $("#date_unloading_date").val();

        const supplier_name = document.querySelectorAll("span")[6].innerText;
        const status = document.getElementsByTagName('span')[12].innerText;
        const s_invoice_number = $('#s_invoice_number').val()
        const s_inv_amount = $('#s_inv_amount').val()
        const s_inv_vat = $('#s_inv_vat').val()
        const s_inv_currency = $('#s_inv_currency').val()
        const c_inv_amount = $('#c_inv_amount').val()
        const s_inv_date = $('#s_inv_date').val()


        console.log(llc, req_id, date_request)
        e.preventDefault();

        $.getJSON('/suppliers/prefin_change', {
            name: llc,
            id: req_id,
            date: date_request,
            pick_up_date: date_loading_plan,
            unloading_date: date_unloading_date,
            sinv_currency: s_inv_currency,
            supp: supplier_name,
            st: status,
            invoice_number: s_invoice_number,
            sinv_amount: s_inv_amount,
            sinv_vat: s_inv_vat,
            cinv_amount: c_inv_amount,
            sinv_date:s_inv_date,
            type: 'POST',
            data: '/suppliers/prefin_change',

            }, function(data) {

                if (data.success) {
                    if (data.success) {
                        $('#successAlert').text(data.success).show();
                        $('#errorAlert').hide();
                    } else {
                        $('#errorAlert').text(data.not).show();
                        $('#successAlert').hide();
                    }
                } else {
                    $('#errorAlert').text(data.not).show();
                    $('#successAlert').hide();
                }
            }

        )

    });

    //Запись в БД
    $('form#myform').bind('click', function(e) {
        const llc = document.querySelector("#select2-tora_red-container").innerText;
        const req_id = document.getElementsByName('id')[0].innerText;
        const date_request = document.querySelector('input#date_order_C').value;
        const date_loading_plan = document.querySelector('input#date_loading_plan').value;
        const date_unloading_date = $("#date_unloading_date").val();

        const supplier_name = document.querySelectorAll("span")[6].innerText;
        const status = document.getElementsByTagName('span')[12].innerText;
        const s_invoice_number = $('#s_invoice_number').val()
        const s_inv_amount = $('#s_inv_amount').val()
        const s_inv_vat = $('#s_inv_vat').val()
        const s_inv_currency = $('#s_inv_currency').val()
        const c_inv_amount = $('#c_inv_amount').val()
        const s_inv_date = $('#s_inv_date').val()
        const work_id = $("#prefin")


        console.log(llc, req_id, date_request)
        e.preventDefault();

        $.getJSON('/suppliers/prefin', {
            name: llc,
            id: req_id,
            date: date_request,
            pick_up_date: date_loading_plan,
            unloading_date: date_unloading_date,
            sinv_currency: s_inv_currency,
            supp: supplier_name,
            st: status,
            invoice_number: s_invoice_number,
            sinv_amount: s_inv_amount,
            sinv_vat: s_inv_vat,
            cinv_amount: c_inv_amount,
            sinv_date:s_inv_date,
            type: 'POST',
            data: '/suppliers/prefin',

        }, function(data) {
            if (data.success) {
                console.log( data.req_id)
                $('#successAlert').text(data.req_id).show();
                $('#errorAlert').hide();
                window.setTimeout(function() { location.reload() }, 1000)
                
                
                
                
            } else {
                console.log(data.not)
                $('#errorAlert').text(data.not).show();
                $('#successAlert').hide();

            }

        });
    });


});