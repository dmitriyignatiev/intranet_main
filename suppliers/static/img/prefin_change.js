$(function() {
    $(document).ready(function() {

   console.log('hi')
        
        

    });
});



    // $('#submit').bind('click', function(e) {
    //     console.log('ready')
    //     e.preventDefault();

    //     $.getJSON('/suppliers/add_supplier_to_db', {
    //         name: $('input[name="name"]').val(),
    //         type: 'POST',
    //         data: '/suppliers/add_supplier_to_db',

    //     }, function(data) {
    //         console.log(data);

    //         if (data.error) {
    //             // $('#successAlert').attr("css", {backgroundColor:"red"});
    //             $('#errorAlert').text(data.error).show();
    //             $('#successAlert').hide();


    //         } else {
    //             window.setTimeout(function() { location.reload() }, 3000);
    //             $('#successAlert').text(data.success).show()
    //             $('#errorAlert').hide();



    //         };

    //     });






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
    // });
    // return false;
// });