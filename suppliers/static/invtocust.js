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









Vue.component('invoiceforms', {
   delimiters: ['[[', ']]'],


   template: `
  
      <div class="form-group mb-2">
           
      <table class="table">
    <thead>
        <tr>
            <th>№</th>
            <th>Товары(работы, услуги)</th>
            <th>Количество</th>
            <th>Ед.</th>
            <th>Цена</th>
            <th>Сумма, без НДС</th>
            <th>Размер НДС</th>
            <th>Итого с НДС</th>
   
            <th>Действия</th>
           
        </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="text" v-model='count' name="#count" class="form-control" />[[count]]</td>
        <td><textarea v-model='description' class="form-control" />[[description]]</td>
        <td><input type="text" v-model='quantity' name='quan-ty' class="form-control" />[[quantity]]</td>
        <td><input type="text" v-model='unit' class="form-control" />[[unit]]</td>
        <td><input type="text" v-model='price' name='price' class="form-control" />[[price]]</td>
        
        
        <td><input type="text" v-model='tt' name='summTotal_w_VAT' class="form-control" />[[countSumm]]</td>
        <td><input type="text" v-model='vat' class="form-control" />[[vat]]</td>
     
        <td><input type="text" class="form-control" v-model='total_t_vat'/>[[countVat]]</td>
       
        <td><button @click='TestAlert'>Записать</button></td>
  
        
        </tr>
    </tbody>
</table>
  
       </div>
 
   `,

   data() {
      return {
         count: "",
         description: "",
         quantity: "",
         unit: "",
         amount:"",
         price: "",
         total:'',
         total_t_vat:this.countVat,
         tt:this.countSumm,
         vat: '',
         selected:'',

      }
   },

   

   computed:{

      countSumm(){
       
            this.tt = parseInt(this.price) * parseInt(this.quantity);
            this.total = this.tt
            return this.tt, this.total
      },

      
      countVat(){
         var c_vat =''
         if (this.price !='' & this.vat !=''){
            c_vat = (100-parseInt(this.vat))/100
            return this.total_t_vat= parseInt(this.total)/c_vat
         }else{
            this.price=this.price }
         
      }
   },

   methods: {
      TestAlert: function () {
         $.getJSON('/suppliers/testVue', {
            count: this.count,
            description: this.description,
            quantity: this.quantity,
            unit: this.unit,
            amount: this.amount,
            price: this.price,
            total: this.total,
            vat: this.vat,
            type: 'POST',
         }, function (data) {
            console.log(data)
         });
      }
   }

})




const helloWorld = new Vue({
   delimiters: ['[[', ']]'],
   el: '#helloVue',

   data: {
     
      invs:invoices,
    
      inv:[
         {'path': '', 'invoice_number': '11' },
         {'path': '', 'invoice_number': '12' }
      ],
      message: 'This is the message',
      name: ""
   },

   methods: {
   },


});









