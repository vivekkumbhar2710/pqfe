// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Core Rejection Analysis', {
	core_warehouse(frm) {
        if (frm.doc.core_warehouse){
            frm.doc.core_rejection_details.forEach(function(i){
                i.core_warehouse = frm.doc.core_warehouse;
            });
           
        } frm.refresh_field('core_rejection_details');
    },
	transaction_date(frm) {
        if (frm.doc.transaction_date){
            frm.doc.core_rejection_details.forEach(function(i){
                i.transaction_date = frm.doc.transaction_date;
            });
           
        } frm.refresh_field('core_rejection_details');
    }
}); 
 
