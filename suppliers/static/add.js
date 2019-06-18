$(document).ready(function(){
    console.log('ready')

    $('form#myform').bind('click', function(e){
    const llc=document.querySelector("#select2-tora_red-container").innerText;
    const req_id=document.getElementsByName('id')[0].innerText;
    
    console.log(llc, req_id)
    e.preventDefault();
  
    $.getJSON('/suppliers/prefin', {
      name:llc, 
      id:req_id,
      type:'POST',
      data:'/suppliers/prefin',
     
    
  }, function(data){
     
  
    if(data.success){
      console.log(data.success)
    }else{
      console.log(data.not)
    }
  
  };
  
  );
    });
});