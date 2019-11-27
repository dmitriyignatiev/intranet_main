

function ShowNewSupp(event) {



  const target = event.target
  const tableNode = target.parentElement.parentElement.children
  const newSupp = tableNode[4]
  const x = target.parentElement.parentElement.parentElement.parentElement
  const z = target.parentNode.parentNode.parentNode.parentElement.childNodes[1].childNodes[1].childNodes[7]

  z.setAttribute("style", "display:block;  box-shadow: 12px 12px 2px 1px rgba(187, 255, 0, 0.2)")
  z.style.backgroundColor = "yellow"

  newSupp.setAttribute("style", "display:block;  box-shadow: 12px 12px 2px 1px rgba(187, 255, 0, 0.2)")
  newSupp.style.backgroundColor = "yellow"

  console.log(target)

}


function HideNewSupp(event) {
  const target = event.target
  const tableNode = target.parentElement.parentElement.children
  const newSupp = tableNode[4]
  const x = target.parentElement.parentElement.parentElement.parentElement
  const z = target.parentNode.parentNode.parentNode.parentElement.childNodes[1].childNodes[1].childNodes[7]
  console.log(z)
  z.setAttribute("style", "display:none")


  newSupp.setAttribute("style", "display:none")

}







function doneSupp(event) {
  const target = event.target
  const supp_name = target.parentElement.parentElement.childNodes[7].innerHTML
  const inv_amount = target.parentElement.parentElement.childNodes[11].childNodes[6].childNodes[0].value
  const inv_number = target.parentElement.parentElement.childNodes[13].childNodes[6].childNodes[0].value
  const inv_date = target.parentElement.parentElement.childNodes[15].childNodes[6].childNodes[0].value
  const inv_deadline = '123'
  console.log(target.parentElement.parentElement.childNodes[17].childNodes[5].childNodes[0].value)


}

function addInv(event) {
  const target = event.target
  const supp_name = target.parentElement.parentElement.childNodes[7].innerHTML
  const inv_amount = target.parentElement.parentElement.childNodes[11].childNodes[6].childNodes[0].value
  const inv_number = target.parentElement.parentElement.childNodes[13].childNodes[6].childNodes[0].value
  const inv_date = target.parentElement.parentElement.childNodes[15].childNodes[6].childNodes[0].value
  const inv_deadline = target.parentElement.parentElement.childNodes[17].childNodes[5].childNodes[0].value
  const vat = target.parentElement.parentElement.childNodes[19].childNodes[6].childNodes[0].value
  const currency = target.parentElement.parentElement.childNodes[21].childNodes[6].childNodes[0].value
  console.log(inv_deadline)

}

function addSupp(event) {
  const target = event.target

  const fin_id = $("#fin_id")[0].innerHTML
  const supp_id = document.getElementById("addsuppname").value
  const s_inv_number = document.getElementById("formaddinvoice").value
  let s_inv_amount = document.getElementById("formaddsinvamount").value
  const s_inv_date = $("#formaddsinvdate")[0].value
  const s_inv_deadline = $("#formaddsuppinvdeadline")[0].value
  const vat = $("#formaddsuppvat")[0].value
  const currency = $("#formaddsuppcurrency")[0].value

  if (s_inv_amount === "") {
    s_inv_amount = 0
  }


  console.log({
    "fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': s_inv_number,
    "s_inv_amount": s_inv_amount, "s_inv_date": s_inv_date, "s_inv_deadline": s_inv_deadline,
    "vat": vat, "currency": currency
  })



  $.getJSON('/suppliers/add_supp_to_fin', {
    fin_id: fin_id,
    supp_id: supp_id,
    s_inv_number: s_inv_number,
    s_inv_amount: s_inv_amount,
    s_inv_date: s_inv_date,
    s_inv_deadline: s_inv_deadline,
    vat: vat,
    currency: currency,
    type: "POST",
    data: '/suppliers/prefin_change_id_test/' + fin_id
  }, function (data) {
    //  console.log(data)

    if (data.success) {
      $("#successAlertaddSupp").text(data.success).show()
      window.setTimeout(function () { location.reload() }, 1000)
      $("#errorAlertaddSupp").text(data.error).hide()
    }
    else { $("#errorAlertaddSupp").text(data.error).show() }




  })

}

function addSuppForm() {
  const udiv = document.getElementById('addSupp');
  udiv.setAttribute("style", 'dislay:block; background:yellow;  margin-left:150px')
}

function closeAddSuppForm() {
  udiv = document.getElementById("addSupp")
  udiv.setAttribute("style", "display:none")
  $("#errorAlertaddSupp").hide()
}

function deleteSupp(event) {
  const target = event.target
  const fin_id = $("#fin_id")[0].innerHTML
  const supp_id = target.parentNode.parentNode.childNodes[5].innerHTML

  $.getJSON('/suppliers/dell_supp_from_fin', {
    fin_id: fin_id,
    supp_id: supp_id,
    type: "POST",
    data: '/suppliers/prefin_change_id_test/' + fin_id

  }, function (data) {
    console.log(data.success)
  })


}

//записываем основной счет
function addInvtoSup(event) {
  event.preventDefault()
  const target = event.target.parentNode
  const x = target.id
  const inv_id_list = document.querySelectorAll(`[id=${CSS.escape(x)}]`)
  const fin_id = $("#fin_id")[0].innerHTML
  const supp_id = target.parentNode.parentNode.childNodes[5].innerHTML
  const inv_summ = inv_id_list[0].childNodes[1].value;
  const inv_number = inv_id_list[1].childNodes[1].value;
  const inv_date = inv_id_list[2].childNodes[1].value;

  const inv_date_d = inv_id_list[3].childNodes[1].value;
  const inv_vat = inv_id_list[4].childNodes[0].value;
  const inv_currency = inv_id_list[5].childNodes[1].value;
  const invoice_id = inv_id_list[6].id
  
  console.log({'inv_id':invoice_id,
    "fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': inv_number,
    "s_inv_amount": inv_summ, "s_inv_date": inv_date, "s_inv_deadline": inv_date_d,
    "vat": inv_vat, "currency": inv_currency
  })

  $.getJSON('/suppliers/add_inv_to_supp', {
    supp_id:supp_id,
    fin_id:fin_id,
    invoice_id:invoice_id,
    s_inv_number: inv_number,
    s_inv_amount: inv_summ,
    s_inv_date: inv_date,
    s_inv_deadline: inv_date_d,
    vat: inv_vat,
    currency: inv_currency,
    type:'POST',
    data: window.location.href

  }, function(data){
    console.log(data)
  })

}

function delInvfromSup(event) {
  event.preventDefault()
  const target = event.target.parentNode
  const x = target.id
  const inv_id_list = document.querySelectorAll(`[id=${CSS.escape(x)}]`)
  const fin_id = $("#fin_id")[0].innerHTML
  const supp_id = target.parentNode.parentNode.childNodes[5].innerHTML
  const inv_summ = inv_id_list[0].childNodes[1].value;
  const inv_number = inv_id_list[1].childNodes[1].value;
  const inv_date = inv_id_list[2].childNodes[1].value;

  const inv_date_d = inv_id_list[3].childNodes[1].value;
  const inv_vat = inv_id_list[4].childNodes[0].value;
  const inv_currency = inv_id_list[5].childNodes[1].value;
  const invoice_id = inv_id_list[6].id
  
  console.log({'inv_id':invoice_id,
    "fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': inv_number,
    "s_inv_amount": inv_summ, "s_inv_date": inv_date, "s_inv_deadline": inv_date_d,
    "vat": inv_vat, "currency": inv_currency
  })

  $.getJSON('/suppliers/del_inv_from_supp', {
    supp_id:supp_id,
    fin_id:fin_id,
    invoice_id:invoice_id,
    s_inv_number: inv_number,
    s_inv_amount: inv_summ,
    s_inv_date: inv_date,
    s_inv_deadline: inv_date_d,
    vat: inv_vat,
    currency: inv_currency,
    type:'POST',
    data: window.location.href

  }, function(data){
    console.log(data)
  })

}





jQuery(function ($) {
  $(function () {
    $(document).ready(function () {
      $.fn.select2.defaults.reset();
      $('#name').select2({ width: '100%' });
      $('#tora_red').select2({ width: '100%' });
      $('#type_of_truck').select2({ width: '100%' });
      $('#status').select2({ width: '100%' });
      
     
      $('#check_inn').select2({ width: '100%' });
      $('#inn').select2({ width: '100%' });
      $('#s_n_all_invoices').select2({ width: '100%' });
      $('select#supp_all_invoices').select2({ width: '100%' });
      $('select#commision').select2({ width: '100%' });
      $('select#name_tr').select2({ width: '100%' });
      $('select#transit').select2({ width: '100' });
      $('select#transit').select2({ width: '100' });
      $('select#our_company').select2({ width: '100' });
      $('select#our_bank').select2({ width: '100' });
      $('select#date_payment').select2({ width: '100' });
      $('select#addsuppname').select2({ width: '100' })

    });

  }

  )
})







