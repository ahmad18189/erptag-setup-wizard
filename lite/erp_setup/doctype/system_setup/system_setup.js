// Copyright (c) 2020, eng.ahmed-madi@hotmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('System Setup', {
	refresh: function(frm) {
		frm.disable_save();
		if(!frm.doc.status){
			frm.set_value('status', "Employees and Users Setup");
		}
		if(!frm.doc.annual_leave_type){
			frm.set_value('annual_leave_type', "30 Days With Holidays");
		}
		change_status(frm);
		// console.log(cur_page);
		
		// var sections = ['employees_and_users_setup', 'roles_setup','items_setup',
		// 'customers_setup', 'suppliers_setup', 'warehouses_setup'];

		
		// $.each(sections, function( index, value ) {
		// 	let section_status = frm.doc.status.toLowerCase().replace(/\s/g, '_');
		//  	if(section_status !== value){
		//  		frm.set_df_property(value, "hidden", 1);
		//  	}
		//  	else{
		//  		frm.set_df_property(value, "hidden", 0);
		//  	}

		// });

		frm.add_custom_button(__('Save'), function() {
			frappe.call({
				method: "setup_system",
				doc: frm.doc,
				freeze: true,
				freeze_message: "Uploading...",
				callback: function(){
					frm.refresh();
					frm.page.set_indicator(frm.doc.status, "orange");
					// if (frm.doc.status == "Complete"){
					// 	frm.page.set_indicator(frm.doc.status, "green");
					// 	window.location.href = "/desk";
					// }
				}
			});
		}).addClass("btn-primary");

	},
	status: function(frm){
		change_status(frm);
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
	},
	no_items: function(frm){
		if (frm.doc.no_items){
			frm.set_value("items_attachment", "")
		}
	},
	no_customers: function(frm){
		if (frm.doc.no_customers){
			frm.set_value("customers_attachment", "")
		}
	},
	no_suppliers: function(frm){
		if (frm.doc.no_suppliers){
			frm.set_value("suppliers_attachment", "")
		}
	},
	no_warehouses: function(frm){
		if (frm.doc.no_warehouses){
			frm.set_value("warehouses_attachment", "")
		}
	},
});

function change_status(frm){
	var sections = ['employees_and_users_setup','items_setup',
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

}