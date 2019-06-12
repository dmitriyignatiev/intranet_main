


$(function() {
    $(document).ready(function() {
       
        $('#name').select2();
        $('#tora_red').select2();
        $('#type_of_truck').select2();
    
    });

  
 
    $('#submit').bind('click', function(e){
        console.log('ready')
        e.preventDefault();

        $.getJSON('/suppliers/add_supplier_to_db', {
            name: $('input[name="name"]').val(),
            type:'POST',
            data:'/suppliers/add_supplier_to_db',

        }, function(data){
            console.log(data);
            
            if (data.error){
                // $('#successAlert').attr("css", {backgroundColor:"red"});
                $('#successAlert').text(data.error).show();
                
               
            }else{
                window.setTimeout(function(){location.reload()},3000);
                 $('#successAlert').text(data.success).show()
                 
                 
                
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





   
