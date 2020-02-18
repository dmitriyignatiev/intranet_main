

$(document).ready(function() {
    $('.js-example-basic-single').select2();
 

});



Vue.component('v-select', VueSelect.VueSelect)

var app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
      selected: [], // make selected an array
      options: [{"id":20,"supp_name":"test1"},{"id":21,"supp_name":"test2"},{"id":34,"supp_name":"supertest"}]
    },
    watch: {
      options: {
        immediate: true,
        handler (options) {
          // initialise to the "supp_name" from options
          this.selected = options.map(({ supp_name }) => supp_name)
        }
      }
    }
  })










