// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

var item_code = []
frappe.ui.form.on('Material Conversion', {
	onload:function(frm){
		frm.doc.input_material.forEach(row=>{
			row.posting_date = frm.doc.posting_date
		})
		frm.doc.output_material.forEach(row=>{
			row.posting_date = frm.doc.posting_date
		})
	},
    setup: function(frm) {
        frm.set_query("item_code", "input_material", function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters:{
					'item_group' :  d.item_group,
				}
            };
        });
		frm.set_query("item_code", "output_material", function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters:{
					'item_group' :  d.item_group,
				}
            };
        });
		frm.set_query("warehouse", "input_material", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					  ["Warehouse", 'company', '=', frm.doc.company]
					]
				};
			});
			
			frm.set_query("warehouse", "output_material", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					  ["Warehouse", 'company', '=', frm.doc.company]
					]
				};
			});
    },
	posting_date:function(frm){
		frm.doc.input_material.forEach(row=>{
			row.posting_date = frm.doc.posting_date
		})
	}
});



// Input Material For Material Conversion

frappe.ui.form.on('Input Material For Material Conversion', {
	

	item_code:function(frm)
	{
		frm.call({
				method:'get_value_per_unit_for_input',
				doc: frm.doc
		});
	},
	
	quantity:function(frm)
	{
		frm.call({
				method:'total_weight_on_input_material',
				doc: frm.doc,
				callback:(r)=>{
					refresh_field["input_total_weight_conversion"]
				}
		});
	},

	input_material_add:function(frm){
		item_code = []
		frm.doc.input_material.forEach(row=>{
			row.posting_date = frm.doc.posting_date
			item_code.push(row.item_code)
		})
		refresh_field["output_material"]

		frm.fields_dict['input_material'].grid.get_field('item_code').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item", 'company', '=', frm.doc.company],
				]
			};
		};
		frm.fields_dict['input_material'].grid.get_field('item_group').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item Group", 'company', '=', frm.doc.company],
				]
			};
		};
		frm.refresh_field('input_material');
	},

	input_material_remove: function(frm) {
		item_code = []
		frm.doc.input_material.forEach(row=>{
			item_code.push(row.item_code)
		})
        frm.call({
            method: 'call_method',
            doc: frm.doc
        });
    },
	warehouse:function(frm)
	{
		frm.call({
				method:'get_available_quantity_input_material',
				doc: frm.doc
		});
	}
});



frappe.ui.form.on('Output Material For Material Conversion', {
	
	setup:function(frm){
		item_code = []
		frm.doc.input_material.forEach(row=>{
			item_code.push(row.item_code)
		})
	
		frm.fields_dict['output_material'].grid.get_field('posting_item_code').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item", 'name', 'in', item_code],
				]
			};
		};
		frm.refresh_field('output_material');
	},
	quantity:function(frm)
	{
		frm.call({
				method:'call_method_output',
				doc: frm.doc
		});
	},
	item_code:function(frm)
	{
		frm.call({
				method:'get_value_per_unit_for_output',
				doc: frm.doc
		});
	},
	output_material_add: function(frm){
		frm.doc.output_material.forEach(row=>{
			row.posting_date = frm.doc.posting_date
		})
		refresh_field["posting_date"]

		item_code = []
		frm.doc.input_material.forEach(row=>{
			item_code.push(row.item_code)
		})
	
		frm.fields_dict['output_material'].grid.get_field('posting_item_code').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item", 'name', 'in', item_code],
				]
			};
		};
		frm.fields_dict['output_material'].grid.get_field('item_group').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item Group", 'company', '=', frm.doc.company],
				]
			};
		};
		frm.refresh_field('output_material');
	},
	output_material_remove: function(frm) {
		frm.fields_dict['output_material'].grid.get_field('item_group').get_query = function (doc,cdt,cdn) {
			return {
				filters: [
					["Item Group", 'company', '=', frm.doc.company],
				]
			};
		};
		frm.refresh_field('output_material');

        frm.call({
            method: 'call_method_output',
            doc: frm.doc
        });
    },
	warehouse:function(frm)
	{
		frm.call({
				method:'get_available_quantity_output_material',
				doc: frm.doc
		});
	},
	posting_item_code:function(frm){
		
	}
});













// // Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// // For license information, please see license.txt


// frappe.ui.form.on('Material Conversion', {
// 	onload:function(frm){
// 		frm.doc.input_material.forEach(row=>{
// 			row.posting_date = frm.doc.posting_date
// 		})
// 		frm.doc.output_material.forEach(row=>{
// 			row.posting_date = frm.doc.posting_date
// 		})
// 	},
//     setup: function(frm) {
//         frm.set_query("item_code", "input_material", function (doc, cdt, cdn) {
//             let d = locals[cdt][cdn];
//             return {
//                 filters:{
// 					'item_group' :  d.item_group,
// 				}
//             };
//         });
//     },
// 	posting_date:function(frm){
// 		frm.doc.input_material.forEach(row=>{
// 			row.posting_date = frm.doc.posting_date
// 		})
// 	}
// });

// frappe.ui.form.on('Material Conversion', {
//     setup: function(frm) {
//         frm.set_query("item_code", "output_material", function (doc, cdt, cdn) {
//             let d = locals[cdt][cdn];
//             return {
//                 filters:{
// 					'item_group' :  d.item_group,
// 				}
//             };
//         });
//     }
// });

// frappe.ui.form.on('Input Material For Material Conversion', {
// 	item_code:function(frm)
// 	{
// 		frm.call({
// 				method:'get_value_per_unit_for_input',
// 				doc: frm.doc
// 		});
// 	},
	
// 	quantity:function(frm)
// 	{
// 		frm.call({
// 				method:'total_weight_on_input_material',
// 				doc: frm.doc
// 		});
// 	},
// });

// frappe.ui.form.on('Input Material For Material Conversion', {
//     quantity: function(frm) {
//         frm.call({
//             method: 'call_method',
//             doc: frm.doc
//         });
//     },
// 	input_material_add:function(frm){
// 		frm.doc.input_material.forEach(row=>{
// 			row.posting_date = frm.doc.posting_date
// 		})
// 	},

// 	input_material_remove: function(frm) {
//         frm.call({
//             method: 'call_method',
//             doc: frm.doc
//         });
//     },
// });


// // frappe.ui.form.on('Input Material For Material Conversion', {
// // 	quantity:function(frm)
// // 	{
// // 		frm.call({
// // 				method:'call_method_input_material_total_weight',
// // 				doc: frm.doc
// // 		});
// // 	}
// // });



// frappe.ui.form.on('Output Material For Material Conversion', {
// 	quantity:function(frm)
// 	{
// 		frm.call({
// 				method:'call_method_output',
// 				doc: frm.doc
// 		});
// 	}
// });

// frappe.ui.form.on('Output Material For Material Conversion', {
// 	quantity:function(frm)
// 	{
// 		frm.call({
// 				method:'total_weight_on_output_material',
// 				doc: frm.doc
// 		});
// 	},
// 	item_code:function(frm)
// 	{
// 		frm.call({
// 				method:'get_value_per_unit_for_output',
// 				doc: frm.doc
// 		});
// 	},
	
// });




 
// frappe.ui.form.on('Input Material For Material Conversion', {
// 	warehouse:function(frm)
// 	{
// 		frm.call({
// 				method:'get_available_quantity_input_material',
// 				doc: frm.doc
// 		});
// 	}
// });

// frappe.ui.form.on('Output Material For Material Conversion', {
// 	warehouse:function(frm)
// 	{
// 		frm.call({
// 				method:'get_available_quantity_output_material',
// 				doc: frm.doc
// 		});
// 	}
// });

// frappe.ui.form.on('Material Conversion', {
// 	setup: function (frm) {
// 	  var company_field = 'company';
//         // frm.set_query("operator_id", function(doc) {
//         //     return {
//         //         filters: [
//         //             ["Operator Master", company_field, '=', frm.doc.company],
//         //          ]
//         //     };
//         // });
        
//         frm.set_query("warehouse", "input_material", function(doc, cdt, cdn) {
// 		let d = locals[cdt][cdn];
// 		return {
// 			filters: [
//         		  ["Warehouse", company_field, '=', frm.doc.company]
// 				]
// 			};
//     	});
    	
//     	frm.set_query("warehouse", "output_material", function(doc, cdt, cdn) {
// 		let d = locals[cdt][cdn];
// 		return {
// 			filters: [
//         		  ["Warehouse", company_field, '=', frm.doc.company]
// 				]
// 			};
//     	});
		
// 	}
// });
 

// frappe.ui.form.on('Output Material For Material Conversion', {
// 	quantity:function(frm)
// 	{
// 		frm.call({
// 				method:'call_method_output',
// 				doc: frm.doc
// 		});
// 	},
// 	output_material_remove: function(frm) {
//         frm.call({
//             method: 'call_method_output',
//             doc: frm.doc
//         });
//     },
// }); 


