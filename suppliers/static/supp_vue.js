
let body = `
{allSuppliers {
    edges {
      node {
        id, llcName,
        prefin {
          id
        }
      }
    }
  }}

`


Vue.component('v-select', VueSelect.VueSelect)

new Vue({
    delimiters: ['[[', ']]'],
    el: "#supp-app",
    data: {
        selected:"",
        suppliers:[
            
        ],
        clickCount:'',
        selected:"",
        new_supplier:{
            name:'',
            inn:'',

        },
        success:{
            SuplierAdd:''
        },
        error:{
            SupplierError: ''
        },
        filterSuppliers:[

        ]
       
    },
    created(){
        this.getSuppliers()
    },
    mounted: function() {
    
      },

    updated: function() {
        if (this.new_supplier.name != ""){
           
        }else{(console.log('test update'))}
        
    },

    computed: {
        compSuppliers: function(){
            compSuppliers = this.suppliers
            return compSuppliers
        }
    },
    

    methods:{
        addCostSupplier(){
            alert('cost')
        },

        supplier_f(){
            console.log(this.selected)
        },

        addSuppPrefin(){
             vm = this
            $.getJSON('/suppliers/add_supplier_to_prefin',{
                name: vm.selected,
               
                type:'POST',
                data:'/suppliers/prefin_change_id_test/'
            }, function(data){
                console.log(data)
            })

        },


        getSuppliers:function(){
            
            axios({
                url:'/graphql',
                method: 'post',
                data:{
                    query:body
                }
            })
                .then((response) => {
                    this.suppliers = response.data.data.allSuppliers.edges 
                    console.log(response)
                })

               
             
                
            },

        addSupplier: function() {
            vm=this,
            $.getJSON('/suppliers/addts', {
                
                name:vm.new_supplier.name,
                inn:vm.new_supplier.inn,
                type:'POST',
                data:'/suppliers/prefin_change_id_test/' + fin_id
            }, function(data) {
                let new_supplier=vm.new_supplier
                console.log(data)
                new_supplier.name=data.response
                console.log(new_supplier.name)
                console.log(vm.new_supplier)
                vm.getSuppliers()

            })

            
              
           

        },

        addNewSuppplier:function(){
            this.suppliers.push(this.new_supplier)
        },

        getFilterSuppliersPrefin(){
            vm = this,
            $.getJSON('/api/suppliers',{
                name:vm.selected,
                type:'POST',
                data:'/suppliers/prefin_change_id_test/' + fin_id
            }, function(data){
                console.log(data[0])
                vm.filterSuppliers.push(data[0].name)
            }
            )
        },

    },

    watch: {
        suppliers: {
            handler: function(newVal){
                if(this.new_supplier.name !=''){
                    
                    console.log(newVal)
                }
                
               
                    
                    
                    
               
            },
            deep:true,
        },

        
    }


})







