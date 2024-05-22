// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Material Return', {
    setup: function(frm) {
        frm.set_query("supplier_id", function() {
            return {
                filters: [
					["Supplier", 'company', '=', frm.doc.company],
				]
            };
        }),
        
        frm.set_query("purchase_order", "material_return", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ["Purchase Order", 'supplier', '=', frm.doc.supplier_id]
                ]
            };
        }),

		frm.set_query("item", "material_return", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ["Item", 'company', '=', frm.doc.company]
                ]
            };
        }),

		frm.set_query("source_warehouse", "material_return", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ["Warehouse", 'company', '=', frm.doc.company]
                   
                ]
            };
        });
    },
	date:function(frm){
		frm.doc.material_return.forEach(row=>{
			row.date = frm.doc.date
		})
	},
	company:function(frm){
		frm.doc.supplier_id = ""
		refresh_field("supplier_id")
	}
});


frappe.ui.form.on('Child Purchase Material Return',{
	
	purchase_order:function(frm){
		frm.call({
			method:'get_rate',
			doc:frm.doc
            
		})
	},
	material_return_add:function(frm,cdt,cdn){
		var d=locals[cdt][cdn]
		d.date = frm.doc.date
	},
	item:function(frm){
		frm.call({
			method:"get_rate",
			doc:frm.doc
		})
	},
    source_warehouse:function(frm,cdt,cdn){
        var d = locals[cdt][cdn]
        if(d.item){
            frm.call({
                method:'get_available_qty',
                doc:frm.doc,
            })
        }else{
            frappe.msgprint({
                title: 'Warning',
                indicator: 'red',
                message:'Select Item before selecting warehouse'
            });
        }
    }
})
