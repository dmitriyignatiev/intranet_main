$(document).ready(function() {
    console.log('ready')

    $('#re_write').bind('click', function(e) {


        const llc = document.querySelector("#select2-tora_red-container").innerText;
        const req_id = document.getElementsByName('id')[0].innerText;
        const date_request = document.querySelector('input#date_order_C').value;


        $.getJSON('/suppliers/prefin_change', {
                name: llc,
                id: req_id,
                date: date_request,
                type: 'POST',
                data: '/suppliers/prefin_change',

            }, function(data) {

                if (data.success) {
                    $('#successAlert').text(data.success).show();
                    $('#errorAlert').hide();
                } else {
                    $('#errorAlert').text(data.not).show();
                    $('#successAlert').hide();
                }
            }

        )

    });


    $('form#myform').bind('click', function(e) {
        const llc = document.querySelector("#select2-tora_red-container").innerText;
        const req_id = document.getElementsByName('id')[0].innerText;
        const date_request = document.querySelector('input#date_order_C').value;

        const supplier_name = document.querySelectorAll("span")[6].innerText





        console.log(llc, req_id, date_request)
        e.preventDefault();

        $.getJSON('/suppliers/prefin', {
            name: llc,
            id: req_id,
            date: date_request,
            supp: supplier_name,
            type: 'POST',
            data: '/suppliers/prefin',

        }, function(data) {
            if (data.success) {
                console.log(data.success)
                $('#successAlert').text(data.success).show();
                $('#errorAlert').hide();

            } else {
                console.log(data.not)
                $('#errorAlert').text(data.not).show();
                $('#successAlert').hide();
            }
        });
    });


});