
$(function(){
    $('#cust').select2();
   
   
        $('a#submit').bind('click', function() {
            
           
            var b = document.getElementById('date').valueAsDate;
            b = b.toISOString().slice(0,10);
            
            console.log(b);
           

            $.getJSON('/process', {
                x : $('input[x="name"]').val(),
                y:b
               
            }, function(data){
                console.log(data) 
                if (data!='dima'){
                    $("#result").text(data.name + data.date);
                    console.log(data)
                }else{
                    $("#result").text(data.ups)
                }
                
            });
            return false;
        });
    });