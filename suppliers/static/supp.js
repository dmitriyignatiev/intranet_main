
jQuery(function($) {
$(function() {
    $(document).ready(function() {
        $.fn.select2.defaults.reset();
        $('#name').select2({width:'100%'});
        $('#tora_red').select2({width:'100%'});
        $('#type_of_truck').select2({width:'100%'});
        $('#status').select2({width:'100%'});
        $('#s_inv_currency').select2({width:'100%'});
        $('#s_inv_vat').select2({width:'100%'});
        $('#check_inn').select2({width:'100%'});
        $('#inn').select2({width:'100%'});
        $('#s_n_all_invoices').select2({width:'100%'});
        $('select#supp_all_invoices').select2({width:'100%'});
        $('select#commision').select2({width:'100%' });
        $('select#name_tr').select2({width:'100%' });
        $('select#transit').select2({width:'100'});
        $('select#transit').select2({width:'100'});

    });

    



    $('#submit').bind('click', function(e) {
        console.log('ready')
        e.preventDefault();

        $.getJSON('/suppliers/add_supplier_to_db', {
            name: $('input[name="name"]').val(),
            inn: $('#inn').val(),
            type: 'POST',
            data: '/suppliers/add_supplier_to_db',

        }, function(data) {
            console.log(data);

            if (data.error) {
                // $('#successAlert').attr("css", {backgroundColor:"red"});
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();


            } else {
                window.setTimeout(function() { location.reload() }, 3000);
                $('#successAlert').text(data.success).show()
                $('#errorAlert').hide();



            };

        });






        //     $('#submit').bind('click', function(e){

        //         e.preventDefault();

        //         var name = $('input[name="name"]').val();
        //         console.log(name);
        //         var credit = $('input[name="credit"]').val();
        //         console.log(credit);

        //         req = $.ajax({

        //             url: '/suppliers/add_supplier_to_db',
        //             type: 'GET', 
        //             data:{name:name},

        //         });

        //         req.done(function(data){
        //             $('#content').html(data);

        //         });
        //     });


        // });
    });
    return false;
});
});