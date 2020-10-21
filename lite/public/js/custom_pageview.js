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

<style>
.progress-bar-animated {
    /* -webkit-animation: progress-bar-stripes 1s linear infinite; */
    animation: progress-bar-stripes 2s linear infinite;
}
.progress-bar-striped {
    background-image: linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);
    background-size: 2rem 2rem;
}
</style>

        <div class="modal fade" id="setup_wizard_modal" role="dialog">
          <div class="modal-dialog" style='margin: auto;width: 70%;top: 30px;'>
          
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title"><i class="fa fa-cog" aria-hidden="true"></i> Setup Wizard</h4>
              </div>
              <div class="modal-body" style="">
              
              <!--<div class="modal-body" style="overflow-y: scroll;height: 60rem;">-->


                <div class="container-fluid">
    <div class="row justify-content-center">
        <div class="col-xs-12 text-center p-0 mt-3 mb-2">
            <div class="card px-0 pt-4 pb-0 mt-3 mb-3">
            <!--
                <h2 id="heading">Sign Up Your User Account</h2>
                <p>Fill all form field to go to next step</p>
            -->
                <form id="msform">
                    <!-- progressbar -->
                    <ul id="progressbar">
                        <li class="active" id="account"><strong>Website</strong></li>
                        <li id="personal"><strong>Employees & Users</strong></li>
                        <li id="payment"><strong>Items</strong></li>
                        <li id="customers"><strong>Customers</strong></li>
                        <li id="suppliers"><strong>Suppliers</strong></li>
                        <li id="confirm"><strong>Warehouses</strong></li>
                    </ul>
                    <div class="progress">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuemin="0" aria-valuemax="100"></div>
                    </div> <br> <!-- fieldsets -->
                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Website Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 1 - 7</h2>
                                </div>
                            </div>


                        <div class='row'>
                          <div class='col-xs-6'>
                            <label class="fieldlabels">Upload Your Logo:</label>
                            <input type="button" name="logo" id="logo" class="logo" value='${r.message['logo'] ? r.message['logo'] : 'Attach'}' >
                          </div>

                          <div class='col-xs-2'>
                            <label class="fieldlabels">Main Color: *</label>
                            <input type="color" name="main_color" id="main_color" class="main_color" placeholder="Main Color" 
                            style='height:4rem;' value='${r.message['main_color']}'
                            />
                          </div>

                        </div>
                        
                        </div> <input type="button" name="next" class="next action-button" value="Next" />
                    </fieldset>

                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Employees and Users Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 2 - 7</h2>
                                </div>
                            </div>




                        <div class='row'>
                          <div class='col-xs-6'>

                            
                            <label class="fieldlabels">Annual Leave Type:</label>

                            <select class="form-control" id="annual_leave_type" style='height:4rem;'>
                                <option value="30 Days With Holidays">30 Days With Holidays</option>
                                <option value="21 Days Without Holidays">21 Days Without Holidays</option>
                            </select>
                            <br>

                            <label class="fieldlabels">Download Template:</label>
                            <input type="button" name="users_template" id="users_template" value='Download' />

                            <label class="fieldlabels">Attach:</label>
                            <input type="button" name="users_attach" id="users_attach" class="users_attach" value='${r.message['employees_attachment'] ? r.message['employees_attachment'] : 'Attach'}'>


                          </div>


                        </div>
                        

                        

                        </div> 
                        <input type="button" name="next" class="next action-button" value="Next" />
                        <input type="button" name="previous" class="previous action-button-previous" value="Previous" />
                    </fieldset>
                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Items Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 3 - 7</h2>
                                </div>
                            </div>


                          <div class="row">
                            <div class='col-xs-6'>

                              
                              <label class="fieldlabels" for="no_items">No Items:</label>
                                <input type="checkbox" id="no_items" name="no_items" >

                              <label class="fieldlabels">Download Template:</label>
                              <input type="button" name="items_template" id="items_template" value='Download' />

                              <label class="fieldlabels">Attach:</label>
                              <input type="button" name="items_attach" id="items_attach" class="items_attach" value='${r.message['items_attachment'] ? r.message['items_attachment'] : 'Attach'}'>

                            </div>
                          </div>



                        </div>
                        <input type="button" name="next" class="next action-button" value="Next" />
                        <input type="button" name="previous" class="previous action-button-previous" value="Previous" />
                    </fieldset>



                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Customers Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 4 - 7</h2>
                                </div>
                            </div>

                            <div class="row">
                              <div class='col-xs-6'>

                                
                                <label class="fieldlabels">No Customers:</label>
                                <input type="checkbox" id="no_customers" name="no_customers" >

                                <label class="fieldlabels">Download Template:</label>
                                <input type="button" name="customers_template" id="customers_template" value='Download' />

                                <label class="fieldlabels">Attach:</label>
                                <input type="button" name="customers_attach" id="customers_attach" class="customers_attach" value='${r.message['customers_attachment'] ? r.message['customers_attachment'] : 'Attach'}'>

                              </div>
                          </div>



                        </div>

                        <input type="button" name="next" class="next action-button" value="Next" />
                        <input type="button" name="previous" class="previous action-button-previous" value="Previous" />

                    </fieldset>




                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Suppliers Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 5 - 7</h2>
                                </div>
                            </div>

                            <div class="row">
                              <div class='col-xs-6'>

                                
                                <label class="fieldlabels">No Suppliers:</label>
                                <input type="checkbox" id="no_suppliers" name="no_suppliers" >

                                <label class="fieldlabels">Download Template:</label>
                                <input type="button" name="suppliers_template" id="suppliers_template" value='Download' />

                                <label class="fieldlabels">Attach:</label>
                                <input type="button" name="suppliers_attach" id="suppliers_attach" class="suppliers_attach" value='${r.message['suppliers_attachment'] ? r.message['suppliers_attachment'] : 'Attach'}'>

                              </div>
                          </div>



                        </div>

                        <input type="button" name="next" class="next action-button" value="Next" />
                        <input type="button" name="previous" class="previous action-button-previous" value="Previous" />

                    </fieldset>



                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Warehouses Setup:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 6 - 7</h2>
                                </div>
                            </div>

                            <div class="row">
                              <div class='col-xs-6'>

                                
                                <label class="fieldlabels">No Warehouses:</label>
                                <input type="checkbox" id="no_warehouses" name="no_warehouses" >

                                <label class="fieldlabels">Download Template:</label>
                                <input type="button" name="warehouses_template" id="warehouses_template" value='Download' />

                                <label class="fieldlabels">Attach:</label>
                                <input type="button" name="warehouses_attach" id="warehouses_attach" class="warehouses_attach" value='${r.message['warehouses_attachment'] ? r.message['warehouses_attachment'] : 'Attach'}'>

                              </div>
                          </div>



                        </div>

                        <input type="button" name="next" id='submit_button' class="next action-button" value="Submit" />
                        <input type="button" name="previous" class="previous action-button-previous" value="Previous" />
                    </fieldset>


                    <fieldset>
                        <div class="form-card">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="fs-title">Finish:</h2>
                                </div>
                                <div class="col-5">
                                    <h2 class="steps">Step 7 - 7</h2>
                                </div>
                            </div> <br><br>
                            <h2 class="purple-text text-center"><strong>SUCCESS !</strong></h2> <br>
                            <div class="row justify-content-center">
                                <div class="col-3 text-center"> <img src="https://i.imgur.com/GwStPmg.png" class="fit-image"> </div>
                            </div> <br><br>
                            <div class="row justify-content-center">
                                <div class="col-7 text-center">
                                    <h5 class="purple-text text-center">Successfully Saved</h5>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
</div>




              </div>
             

            </div>
            
          </div>
        </div>







<script>

$(document).ready(function(){

var current_fs, next_fs, previous_fs; //fieldsets
var opacity;
var current = 1;
var steps = $("fieldset").length;

setProgressBar(current);

$(".next").click(function(){

current_fs = $(this).parent();
next_fs = $(this).parent().next();

//Add Class Active
$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

//show the next fieldset
next_fs.show();
//hide the current fieldset with style
current_fs.animate({opacity: 0}, {
step: function(now) {
// for making fielset appear animation
opacity = 1 - now;

current_fs.css({
'display': 'none',
'position': 'relative'
});
next_fs.css({'opacity': opacity});
},
duration: 500
});
setProgressBar(++current);
});

$(".previous").click(function(){

current_fs = $(this).parent();
previous_fs = $(this).parent().prev();

//Remove class active
$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

//show the previous fieldset
previous_fs.show();

//hide the current fieldset with style
current_fs.animate({opacity: 0}, {
step: function(now) {
// for making fielset appear animation
opacity = 1 - now;

current_fs.css({
'display': 'none',
'position': 'relative'
});
previous_fs.css({'opacity': opacity});
},
duration: 500
});
setProgressBar(--current);
});

function setProgressBar(curStep){
var percent = parseFloat(100 / steps) * curStep;
percent = percent.toFixed();
$(".progress-bar")
.css("width",percent+"%")
}

$(".submit").click(function(){
return false;
})

});


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


if(window.location.hostname!='erptag.com'){
  $(window).on("load", get_customer_logo);
}

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


