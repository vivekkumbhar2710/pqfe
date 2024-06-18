// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

let patterns = []
frappe.ui.form.on('Daywise Pouring Schedule', {
	date:function(frm){
		if(frm.doc.date){
			// console.log(frm.doc.date)
			var total = 0
			frm.doc.item_pouring_schedule.forEach(row=>{
				// console.log(row.planned_weight)
				if(row.planning_date==frm.doc.date){
					// console.log(row.planned_weight)
					total+=row.planned_weight
				}
			})
			// console.log(total)
			frm.set_value('daywise_total_weight', total);
			frm.refresh_field("daywise_total_weight")
			
		}
	},
	setup:async function(frm) {

        frm.set_query("item_code", "item_pouring_schedule", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                   ["Item","company","=",doc.company],
				   ["Item","item_group","=","CASTING"]
				]
            };
        });
		
			frm.set_query("pattern","item_pouring_schedule", function(doc,cdt,cdn){
				let d = locals[cdt][cdn]
				// console.log(d.item_code)
				// console.log("Fetching patterns for item_code:", d.item_code);
			    get_pattern(frm,doc,d.item_code)
				// console.log("Available patterns:", patterns);
				
				return {
					filters: [
						["Pattern Master","name","in",patterns]
					],
					
				}
				
			})
			// frm.fields_dict.item_pouring_schedule.grid.get_field("pattern").get_query = async function(doc, cdt, cdn) {
			// 	let d = locals[cdt][cdn];
			// 	console.log("Fetching patterns for item_code:", d.item_code);
			// 	await get_pattern(frm,doc, d.item_code);
			// 	console.log("Available patterns:", patterns);
			// 	// frm.fields_dict.item_pouring_schedule.grid.refresh_field("pattern");
			// 	return {
			// 		filters: [
			// 			["Pattern Master", "name", "in", patterns]
			// 		]
			// 	};
			// }
		}	
	// });

  
	
});

frappe.ui.form.on('Daywise Pouring Schedule Items',{
	item_code:async function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		await get_pattern(frm,frm.doc,d.item_code)
		console.log(patterns)
	},
	

	
})

async function get_pattern(frm,doc,item_code){
  let response = await frappe.call({
		method:"get_patterns",
		doc:doc,
		args:{
			'item_code':item_code
		}
	
	})
	if(response.message){
		patterns = []
		patterns = response.message

}else {
	patterns = [];
}

}