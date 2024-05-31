// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Foundry Rejection Analaysis', {
	rejection_analysis_outsourcing_job_work:function(frm)
	{ 
        frm.clear_table("rejection_details")
		frm.call({
				method:'get_outsourcing_job_work',
				doc: frm.doc
		});
	} 
});

frappe.ui.form.on('Foundry Rejection Analaysis', {
    delivery_note: function (frm) {
        frm.clear_table("rejection_details");
        frm.call({
            method: 'call_in_one',
            doc: frm.doc
        });
        frm.refresh_table("rejection_details");
    },
    sales_invoice: function (frm) {
        frm.clear_table("rejection_details");
        frm.call({
            method: 'call_in_one',
            doc: frm.doc
        });
        frm.refresh_table("rejection_details");
    }
});

frappe.ui.form.on('Rejection Details', {
	is_scrap: function(frm) {     
		frm.call({
			method:'set_target_warehouse_item',
			doc:frm.doc
		})
        frm.refresh_field("target_warehouse_item"),
		frm.refresh_field("scrap_item_name");
       
	}
});

frappe.ui.form.on('Foundry Rejection Analaysis', {
    setup: function(frm) {
            frappe.call({
                method: 'set_filters_for_outsourcing_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
						var k = r.message;
                        // frm.set_query("outsourcing_job_work", "rejection_analysis_outsourcing_job_work", function(doc, cdt, cdn) {
						frm.fields_dict.rejection_analysis_outsourcing_job_work.get_query = function (doc, cdt, cdn) {
					        // let d = locals[cdt][cdn];
                            return {
                                filters: [
									['Subcontracting','name','in', k],
								    ['Subcontracting', 'company', '=', doc.company],
                                    ['Subcontracting', 'in_or_out', '=', "IN"]
                                ]
                            };
                        };
                    }
                }
			});
     } 
});
  
frappe.ui.form.on('Foundry Rejection Analaysis', {
    setup: function(frm) {
            frappe.call({
                method: 'set_filters_for_delivery_note',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
						var k = r.message;
                        // frm.set_query("outsourcing_job_work", "rejection_analysis_outsourcing_job_work", function(doc, cdt, cdn) {
						frm.fields_dict.delivery_note.get_query = function (doc, cdt, cdn) {
					        // let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Delivery Note','name','in', k],
									["Delivery Note", "company", '=', frm.doc.company],// Replace with your actual filter criteria
                                    ["Delivery Note", "customer", '=', frm.doc.customer_id],
                                    ["Delivery Note", "is_return", '=', 1],
                                ]
                            };
                        };
                    }
                }
			});
     } 
});

frappe.ui.form.on('Foundry Rejection Analaysis', {
    setup: function(frm) {
            frappe.call({
                method: 'set_filters_for_sales_invoice',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
						var k = r.message;
                        // frm.set_query("outsourcing_job_work", "rejection_analysis_outsourcing_job_work", function(doc, cdt, cdn) {
						frm.fields_dict.sales_invoice.get_query = function (doc, cdt, cdn) {
					        // let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Sales Invoice','name','in', k],
                                    ["Sales Invoice", "company", '=', frm.doc.company],
                                    ["Sales Invoice", "customer", '=', frm.doc.customer_id],
                                    ["Sales Invoice", "is_return", '=', 1],
                                    ["Sales Invoice", "update_stock", '=', 1],
                                ]
                            };
                        };
                    }
                }
			});
     } 
});

frappe.ui.form.on('Foundry Rejection Analaysis', {
    source_warehouse(frm) {
        if (frm.doc.source_warehouse){
            frm.doc.rejection_details.forEach(function(i){
                i.source_warehouse = frm.doc.source_warehouse;
            });
           
        } frm.refresh_field('rejection_details');
    }
});

frappe.ui.form.on('Rejection Details', {
    item_code: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (frm.doc.source_warehouse) {
            frappe.model.set_value(child.doctype, child.name, 'source_warehouse', frm.doc.source_warehouse);
        }
        frm.refresh_field('rejection_details');
    }
});

frappe.ui.form.on('Foundry Rejection Analaysis', {
    target_warehouse(frm) {
        if (frm.doc.target_warehouse){
            frm.doc.rejection_details.forEach(function(i){
                i.target_warehouse = frm.doc.target_warehouse;
            });
           
        } frm.refresh_field('rejection_details');
    }
})

frappe.ui.form.on('Rejection Details', {
    item_code: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (frm.doc.target_warehouse) {
            frappe.model.set_value(child.doctype, child.name, 'target_warehouse', frm.doc.target_warehouse);
        }
        frm.refresh_field('rejection_details');
    }
});

 