// function writeToLocalStorage(key, value) {
//   localStorage.setItem(key, JSON.stringify(value))
// }
// function readFromLocalStorage(key, v) {
//   if (localStorage.getItem(key)) {
//     v = JSON.parse(localStorage.getItem(key))background-color: #f9f9f9;
//   }
//   return v
// }
// writeToLocalStorage("modules_data_cache", {});
// writeToLocalStorage("current_module_sections", []);
// function process_data(module_name, data) {
//   frappe.module_links[module_name] = []
//   data.forEach(function (section) {
//     section.items.forEach(function (item) {
//       item.route = generate_route(item)
//     })
//   })
// }


$(document).ready((ev) => {




  frappe.call({
    method: "lite.api.get_system_setup_info",
    callback: function (r) {


if(!r.message['logo'] || !r.message['employees_attachment'] || !r.message['items_attachment'] || !r.message['customers_attachment'] || !r.message['suppliers_attachment'] || !r.message['warehouses_attachment']){
  

      $("#body_div #page-desktop .container").prepend(`
        <div class="alert alert-warning alert-dismissible" style='top: 30px;position: relative;margin-left: 250px;'>
        <a href="#" class="close" data-dismiss="alert" aria-label="close" style="color:#8a6d3b">&times;</a>
          <a style="color:#8a6d3b" data-toggle='modal' data-target='#setup_wizard_modal'>
            <i class="fa fa-exclamation-circle" aria-hidden="true"></i> 
            Please click here and follow the steps to set up your account
          </a>
        </div>
        `)




}





      $("#body_div #page-desktop .container").prepend(`




              <link href="/assets/lite/setup_wizard/css/style.css" rel="stylesheet">
              <link href="/assets/lite/setup_wizard/css/responsive.css" rel="stylesheet">
              <link href="/assets/lite/setup_wizard/css/icon_fonts/css/all_icons_min.css" rel="stylesheet">
              <link href="/assets/lite/setup_wizard/css/skins/square/grey.css" rel="stylesheet">



              <style>

                #form_container input[type="checkbox"]{
                  visibility: initial!important;
                }

                #form_container input[type="checkbox"]:checked:before{
                      visibility: hidden;
                }

                #form_container input[type="checkbox"]:before{
                  visibility: hidden;
                }


                #form_container input[type="checkbox"]{
                  background: none!important;
                  background-color: #fff!important;
                  border: none!important;
                  border-radius: 0!important;
                  -webkit-box-shadow: none!important;
                  box-shadow: none!important;
                  -webkit-transition: none!important;
                  color: #999!important;
                  height: 18px!important;
                  font-size: 16px!important;
                  font-weight: 400!important;
                  margin-bottom: 25px!important;
                  padding: 6px 12px 6px 0!important;
                }


              </style>

              <script src="/assets/lite/setup_wizard/js/jquery-3.5.1.min.js"></script>
              <script src="/assets/lite/setup_wizard/js/registration_wizard_func.js"></script>
              <script src="/assets/lite/setup_wizard/js/common_scripts_min.js"></script>




  <div class="modal fade" id="setup_wizard_modal" role="dialog">



    <div id="form_container" class='modal-content'>
      <div class="row">
        <div class="col-lg-5">
          <div id="left_form">
            <figure><img src="/assets/lite/setup_wizard/img/registration_bg.svg" alt=""></figure>
            <h2>Setup Wizard</h2>
            <p>Please follow the steps to complete the setup.</p>
          </div>
        </div>
        <div class="col-lg-7">

          <div id="wizard_container">
            <div id="top-wizard">
              <div id="progressbar"></div>
            </div>
            <!-- /top-wizard -->
            <form>
              <input id="website" name="website" type="text" value="">
              <!-- Leave for security protection, read docs for details -->
              <div id="middle-wizard">

                <div class="step">
                  <h3 class="main_question"><strong>1/6</strong>Website Setup</h3>
                  

                  <div class="row">
                    <div class="col-md-10">
                      <div class="form-group">
                            <input type="button" name="logo" id="logo" class="logo form-control" value='${r.message['logo'] ? r.message['logo'] : 'Attach'}' >
                      </div>
                    </div>
                    <div class="col-md-2">
                      <div class="form-group">
                        <input type="color" name="main_color" id="main_color" class="main_color form-control" placeholder="Main Color" 
                            style='height:4rem;' value='${r.message['main_color']}'/>
                      </div>
                    </div>
                  </div>



                </div>

                <div class="step">
                  <h3 class="main_question"><strong>2/6</strong>Employees and Users Setup</h3>
                  


                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <div class="styled-select">
                          <select id="annual_leave_type">
                                <option value="30 Days With Holidays">30 Days With Holidays</option>
                                <option value="21 Days Without Holidays">21 Days Without Holidays</option>
                            </select>
                        </div>
                      </div>
                    </div>
                  </div>


                  <div class="row">
                    <div class="col-md-9">
                      <div class="form-group">
                          <input type="button" name="users_attach" id="users_attach" class="users_attach form-control" value='${r.message['employees_attachment'] ? r.message['employees_attachment'] : 'Attach'}'>

                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="form-group">
                            <input type="button" name="users_template" id="users_template" class="users_template form-control" value='Download' />
                      </div>
                    </div>
                  </div>

                </div>




                <div class="step">
                  <h3 class="main_question"><strong>3/6</strong>Items Setup</h3>
                  

                  <div class="row">
                    <div class="col-md-1">
                      <div class="form-group">
                        <input type="checkbox" id="no_items" name="no_items" class="no_items form-control" >
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-9">
                      <div class="form-group">
                          <input type="button" name="items_attach" id="items_attach" class="items_attach form-control" value='${r.message['items_attachment'] ? r.message['items_attachment'] : 'Attach'}'>

                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="form-group">
                              <input type="button" name="items_template" id="items_template" class="items_template form-control" value='Download' />
                      </div>
                    </div>
                  </div>


                </div>




                <div class="step">
                  <h3 class="main_question"><strong>4/6</strong>Customers Setup</h3>
                  

                  <div class="row">
                    <div class="col-md-1">
                      <div class="form-group">
                        <input type="checkbox" id="no_customers" name="no_customers" class="no_customers form-control" >
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-9">
                      <div class="form-group">
                          <input type="button" name="customers_attach" id="customers_attach" class="customers_attach form-control" value='${r.message['customers_attachment'] ? r.message['customers_attachment'] : 'Attach'}'>

                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="form-group">
                              <input type="button" name="customers_template" id="customers_template" class="customers_template form-control" value='Download' />
                      </div>
                    </div>
                  </div>


                </div>





                <div class="step">
                  <h3 class="main_question"><strong>5/6</strong>Suppliers Setup</h3>
                  

                  <div class="row">
                    <div class="col-md-1">
                      <div class="form-group">
                        <input type="checkbox" id="no_suppliers" name="no_suppliers" class="no_suppliers form-control" >
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-9">
                      <div class="form-group">
                          <input type="button" name="suppliers_attach" id="suppliers_attach" class="suppliers_attach form-control" value='${r.message['suppliers_attachment'] ? r.message['suppliers_attachment'] : 'Attach'}'>

                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="form-group">
                              <input type="button" name="suppliers_template" id="suppliers_template" class="suppliers_template form-control" value='Download' />
                      </div>
                    </div>
                  </div>


                </div>



                <div class="submit step ">
                  <h3 class="main_question"><strong>6/6</strong>Warehouses Setup</h3>
                  
                  
                  <div class="row">
                    <div class="col-md-1">
                      <div class="form-group">
                        <input type="checkbox" id="no_warehouses" name="no_warehouses" class="no_warehouses form-control" >
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-9">
                      <div class="form-group">
                          <input type="button" name="warehouses_attach" id="warehouses_attach" class="warehouses_attach form-control" value='${r.message['warehouses_attachment'] ? r.message['warehouses_attachment'] : 'Attach'}'>

                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="form-group">
                              <input type="button" name="warehouses_template" id="warehouses_template" class="warehouses_template form-control" value='Download' />
                      </div>
                    </div>
                  </div>

              </div>

              <!-- /middle-wizard -->
              <div id="bottom-wizard">
                <button type="button" name="backward" class="backward">Backward </button>
                <button type="button" name="forward" class="forward">Forward</button>
                <button type="submit" name="process" class="submit" id="submit_button" >Submit</button>
              </div>
              <!-- /bottom-wizard -->
            </form>
          </div>
          <!-- /Wizard container -->
        </div>
      </div><!-- /Row -->
    </div><!-- /Form_container -->
  </div>
  
  



<script>

$("#users_template").click(function() {
    window.open('/assets/lite/downloads/employees.csv');
});

$("#items_template").click(function() {
    window.open('/assets/lite/downloads/items.csv');
});

$("#customers_template").click(function() {
    window.open('/assets/lite/downloads/customers.csv');
});

$("#suppliers_template").click(function() {
    window.open('/assets/lite/downloads/suppliers.csv');
});

$("#warehouses_template").click(function() {
    window.open('/assets/lite/downloads/warehouses.csv');
});




$("#no_items").click(function() {
  if($('#no_items').prop('checked')){
    $("#items_template").prop('disabled', true);
    $("#items_attach").prop('disabled', true);
    $("#items_attach").val('Attach');
  }else{
    $("#items_template").prop('disabled', false);
    $("#items_attach").prop('disabled', false);
  }
});

$("#no_customers").click(function() {
  if($('#no_customers').prop('checked')){
    $("#customers_template").prop('disabled', true);
    $("#customers_attach").prop('disabled', true);
    $("#customers_attach").val('Attach');
  }else{
    $("#customers_template").prop('disabled', false);
    $("#customers_attach").prop('disabled', false);
  }
});

$("#no_suppliers").click(function() {
  if($('#no_suppliers').prop('checked')){
    $("#suppliers_template").prop('disabled', true);
    $("#suppliers_attach").prop('disabled', true);
    $("#suppliers_attach").val('Attach');
  }else{
    $("#suppliers_template").prop('disabled', false);
    $("#suppliers_attach").prop('disabled', false);
  }
});

$("#no_warehouses").click(function() {
  if($('#no_warehouses').prop('checked')){
    $("#warehouses_template").prop('disabled', true);
    $("#warehouses_attach").prop('disabled', true);
    $("#warehouses_attach").val('Attach');
  }else{
    $("#warehouses_template").prop('disabled', false);
    $("#warehouses_attach").prop('disabled', false);
  }
});





$("#logo").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#logo").val(file.file_url);
      }
    });
});

$("#users_attach").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#users_attach").val(file.file_url);
      }
    });
});

$("#items_attach").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#items_attach").val(file.file_url);
      }
    });
});


$("#customers_attach").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#customers_attach").val(file.file_url);
      }
    });
});


$("#suppliers_attach").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#suppliers_attach").val(file.file_url);
      }
    });
});


$("#warehouses_attach").click(function() {
  new frappe.ui.FileUploader({
      folder: 'Home/Attachments',
      allow_multiple: false,
      on_success: file => {
          $("#warehouses_attach").val(file.file_url);
      }
    });
});


$("#submit_button").click(function() {
  edit_system_setup()

});


</script>



        `)






  $("#annual_leave_type").val(r.message['annual_leave_type'])


if(r.message['no_items']==1){
  $("#no_items").attr('checked', 'checked')
      $("#items_template").prop('disabled', true);
    $("#items_attach").prop('disabled', true);
}else{
  $("#no_items").removeAttr('checked')
}



if(r.message['no_customers']==1){
  $("#no_customers").attr('checked', 'checked')
      $("#customers_template").prop('disabled', true);
    $("#customers_attach").prop('disabled', true);
}else{
  $("#no_customers").removeAttr('checked')
}



if(r.message['no_suppliers']==1){
  $("#no_suppliers").attr('checked', 'checked')

    $("#suppliers_template").prop('disabled', true);
    $("#suppliers_attach").prop('disabled', true);
}else{
  $("#no_suppliers").removeAttr('checked')
}



if(r.message['no_warehouses']==1){
  $("#no_warehouses").attr('checked', 'checked')

    $("#warehouses_template").prop('disabled', true);
    $("#warehouses_attach").prop('disabled', true);
}else{
  $("#no_warehouses").removeAttr('checked')
}




    }
  })






})


  $(window).on("load", get_customer_logo);


// $(window).on("hashchange", edit_system_setup);

function edit_system_setup(){


    var logo = $("#logo").val();
    var main_color = $("#main_color").val();

    var annual_leave_type = $("#annual_leave_type").val();
    var users_attach = $("#users_attach").val();
    
    var no_items = $('#no_items').is( ':checked' ) ? 1: 0;
    var items_attach = $("#items_attach").val();

    var no_customers = $('#no_customers').is( ':checked' ) ? 1: 0;
    var customers_attach = $("#customers_attach").val();

    var no_suppliers = $('#no_suppliers').is( ':checked' ) ? 1: 0;
    var suppliers_attach = $("#suppliers_attach").val();

    var no_warehouses = $('#no_warehouses').is( ':checked' ) ? 1: 0;
    var warehouses_attach = $("#warehouses_attach").val();
    
    frappe.call({
        method: "lite.api.edit_system_setup",
        args: {
            logo: logo,
            main_color: main_color,

            annual_leave_type: annual_leave_type,
            users_attach: users_attach,

            no_items: no_items,
            items_attach: items_attach,

            no_customers: no_customers,
            customers_attach: customers_attach,

            no_suppliers: no_suppliers,
            suppliers_attach: suppliers_attach,

            no_warehouses: no_warehouses,
            warehouses_attach: warehouses_attach
        },
        callback: function (r) {
            if (r.message) {
                console.log(r.message)
            }
        }
    })




    // frappe.call({
    //     method: "lite.erp_setup.doctype.system_setup.system_setup.setup_system",
    //     callback: function(){
    //     }
    //   });



}


function get_customer_logo(){

    frappe.call({
        method: "lite.api.get_customer_logo_and_color",
        callback: function (r) {
            if (r.message) {
              
                $("#customer_logo").attr("src", r.message[0]);

                $("#sidenav").css("background-color", r.message[1]);
                $(".btn-primary, .add-filter, .tags-list .tags-list-item .frappe-tag.btn-group, .page-actions .btn-primary").css("background-color", r.message[1]);
            
            }
        }
    })

}


