$(document).ready(function() {
    $('.js-example-basic-single').select2();
});

const invoices = [
    {
        id: 1,
        number: '11',
        test_attr: 
            {
                'id':1,
                'test_key':'test_value_1',
                'test_test_key':'test_value_2'
        
        
        },
            
        
    },

    {
        id: 2,
        number: '12'
    }
]


var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: "#invoicecust",
    data() {
        return{

        
        renderKey: 1,
        user: {
            firstName:'',
        },
        
        invoiceDetails:[
            {
                id: 1,
                number: '11',
                test_attr: 
                    {
                        'id':1,
                        'test_key':'test_value_1',
                        'test_test_key':'test_value_2',
                
                        
                },
              
                test:{},
                invoices: [
                    
                ]
                
            
            },
        
            {
                id: 2,
                number: '12',
                test:{},
                invoices: [
                   
                ]
                
            },

                
        ],
        

            
        
    }   
    },
    created() {
        this.makeId();
    },

    methods:{
        
        makeId:function(){
            let id;
            for(id=0; id<this.invoiceDetails.length; id++){
                console.log(this.createInvoice)
            }
        },

        add_test_1: function(){
            this.invoiceDetails.push(
                {
                    'id': this.id,
                    'number': this.number,
                    'test':'' ,
                    invoices: [
                        
                    ]
                    
                }
            );
            
            this.id = "",
            this.number = "";
            
            
           

            
        },

        add: function(item){
           
           var i;
           for(i=0; i<this.invoiceDetails[item].test['u']; i++){
               console.log(pars)
           }

           console.log(this.invoiceDetails[item].test)
           
            
        },

        addPlus: function(item){
            this.invoiceDetails[item].test = {'u': 1}
            this.invoiceDetails[item].test.u++
            
            for(i=1; i<this.invoiceDetails[item].test.u; i++){
                this.invoiceDetails[item].invoices.push({
                    'description':'',
                    'summ': '',
                    'vat': 18,
                    'total': '',
                
                
                })

            };

           

            
        },

        f_test:function(item){

           console.log(this.invoiceDetails[item].invoices[item].total = parseInt(this.invoiceDetails[item].invoices[item].vat) + parseInt(this.invoiceDetails[item].invoices[item].summ))
            return this.invoiceDetails[item].invoices[item].total = parseInt(this.invoiceDetails[item].invoices[item].vat) + parseInt(this.invoiceDetails[item].invoices[item].summ)
            
        },

      

        watch_function:function(item){
           return parseInt(item.summ) + parsetInt(item.vat)
        },

    },

    computed:{
        myInvoices(){
            return this.invoiceDetails;
        },

    },

    mounted(){
        this.$watch('user', () => console.log('foo'), {deep: true})
        
    },



    watch:{
     'firstName'(val){
         console.log('call', val)
     },

     invoiceDetails:{
         handler: function(){
             let i;
             for(i=0; i<this.invoiceDetails.length; i++){
              
                this.invoiceDetails[i].invoices.filter(function(element){
                    if(element.summ != ''){
                        return element.total = parseInt(element.summ) + parseInt(element.vat)
                    }else{
                        return element.total =''
                    }
                })
               
                
             
             }
         },
         deep:true,
     }
        
    },

    

    
})