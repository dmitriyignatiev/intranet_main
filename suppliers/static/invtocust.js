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


















