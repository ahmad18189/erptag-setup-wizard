// Copyright (c) 2020, eng.ahmed-madi@hotmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('System Setup', {
	refresh: function(frm) {
		frm.disable_save();
		
		var sections = ['employees_and_users_setup', 'roles_setup','items_setup',
		'customers_setup', 'suppliers_setup', 'warehouses_setup'];

		
		$.each(sections, function( index, value ) {
			let section_status = frm.doc.status.toLowerCase().replace(/\s/g, '_');
		 	if(section_status !== value){
		 		frm.set_df_property(value, "hidden", 1);
		 	}
		 	else{
		 		frm.set_df_property(value, "hidden", 0);
		 	}

		});

		frm.add_custom_button(__('Save & Upload'), function() {
			frappe.call({
				method: "setup_system",
				doc: frm.doc,
				freeze: true,
				freeze_message: "Uploading...",
				callback: function(){
					frm.refresh();
				}
			});
		}).addClass("btn-primary");

	},
	employees_button: function(frm){
		window.open('/assets/lite/downloads/employees.csv');
	},
	items_button: function(frm){
		window.open('/assets/lite/downloads/items.csv');
	},
	customers_button: function(frm){
		window.open('/assets/lite/downloads/customers.csv');
	},
	suppliers_button: function(frm){
		window.open('/assets/lite/downloads/suppliers.csv');
	},
	warehouses_button: function(frm){
		window.open('/assets/lite/downloads/warehouses.csv');
	}
});
