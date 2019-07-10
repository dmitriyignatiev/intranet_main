$(document).ready(function() {
    console.log('ready')

    $('form#myform').bind('click', function(e) {
        const llc = document.querySelector("#select2-tora_red-container").innerText;
        const req_id = document.getElementsByName('id')[0].innerText;
        const date_request = document.querySelector('input#date_order_C').value;

        console.log(llc, req_id, date_request)
        e.preventDefault();

        $.getJSON('/suppliers/prefin', {
            name: llc,
            id: req_id,
            data: date_request,
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