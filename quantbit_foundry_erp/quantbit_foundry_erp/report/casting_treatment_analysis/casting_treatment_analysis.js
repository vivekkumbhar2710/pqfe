// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Casting Treatment Analysis"] = {
	"filters": [
		{
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company",
			"reqd":1
        },
        {
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
			"reqd":1
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
			"reqd":1
        },
        {
			fieldname: "item_code",
			label: __("Item Name"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
        {
			fieldname: "contractor",
			label: __("Contractor Name"),
			fieldtype: "MultiSelectList",
			options: "Supplier",
			get_data: function(txt) {
				return frappe.db.get_link_options("Supplier", txt);
			},
			reqd: 0,
		},
        {
			fieldname: "casting_treatment",
			label: __("Casting Treatment"),
			fieldtype: "MultiSelectList",
			options: "Casting Treatment Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Casting Treatment Master", txt);
			},
			reqd: 0,
		},
        // {
        //     "fieldname": "item_code",
        //     "fieldtype": "Link",           
        //     "options": "Item",
		// 	"label": "Item Name"
        // },
		// {
		// 	"fieldname": "casting_treatment",
		// 	"fieldtype": "Link",
		// 	"options": "Casting Treatment Master",
		// 	"label": "Casting Treatment"
		// },	
		// {
        //     "fieldname": "contractor",
        //     "fieldtype": "Link",
        //     "options": "Supplier",
		// 	"label": "Contractor Name",
        // }
	]
};
