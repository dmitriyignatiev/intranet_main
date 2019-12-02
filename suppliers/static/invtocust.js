function addInvFormtoCust() {
   const utable = document.getElementById('formInvcust')
   utable.style.display = 'block'
}

$("#addserviceb").bind("click", function () {

   const utextarea = document.createElement('textarea')
   utextarea.setAttribute("class", "form-control")

   var textnode = document.createTextNode("Water")
   utextarea.appendChild(textnode)
   console.log(utextarea)
   const parrent = document.getElementById("addservicef")
   const up = documen.createElement('p')

   console.log(parrent)
   parrent.appendChild(up)
   up.appendChild(utextarea)
})


// function testforvue(){
//    var my_json=document.getElementById('vuedata').innerHTML
//    // my_json=JSON.stringify(my_json)
//    my_json = my_json.replace(/None/g, '""')
//    my_json = my_json.replace(/'/g, '"')
   
//    my_json=JSON.parse(my_json)
//    console.log(my_json)
//    console.log(typeof(my_json))
// }

var my_json=document.getElementById('vuedata').innerHTML;
var my_json = my_json.replace(/None/g, '""');
var my_json = my_json.replace(/'/g, '"');
   
var my_json=JSON.parse(my_json);

const helloWorld = new Vue({
   delimiters: ['[[', ']]'],
   el:'#helloVue',
   
   data: {
      prefin:[my_json],
      message: 'This is the message',
  
   },
      
 

})



