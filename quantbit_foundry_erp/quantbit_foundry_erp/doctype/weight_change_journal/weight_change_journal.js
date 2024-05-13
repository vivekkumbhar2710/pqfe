// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Weight Change Journal', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Weight Change Journal', {
    item_code: function(frm) {
        frm.call({
            method: 'get_item_weight',
            doc: frm.doc,
        })

    },
});