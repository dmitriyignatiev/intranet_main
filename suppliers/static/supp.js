


$(function(){
    $(document).ready(function() {
        $('#name').select2();
    });

 
    // $('#submit').bind('click', function(e){
    //     e.preventDefault();

    //     $.getJSON('/suppliers/add_supplier_to_db', {
    //         name: $('input[name="name"]').val(),
    //     }, function(data){
    //         console.log(data)
    //         if (data.error){

    //             $('#successAlert').text(data.error).show();           
               
    //         }else{
    //              $('#successAlert').text(data.success).show();
                
    //         }

    //     });

        
    // });
   
   


    $('#submit').bind('click', function(e){
        
        e.preventDefault();
        
        var name = $('input[name="name"]').val();
        console.log(name);
        var credit = $('input[name="credit"]').val();
        console.log(credit);

        req = $.ajax({
            
            url: '/suppliers/add_supplier_to_db',
            type: 'GET', 
            data:{name:name},
            
        });

        req.done(function(data){
            $('#content').html(data);
            
        });
    });

    
});

