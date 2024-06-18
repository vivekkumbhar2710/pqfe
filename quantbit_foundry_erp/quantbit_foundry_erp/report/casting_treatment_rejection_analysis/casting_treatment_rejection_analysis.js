// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Casting Treatment Rejection Analysis"] = {
	"filters": [
		{
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company",
			"reqd" : 1
        }, 
        {
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
			"reqd" : 1
        }, 
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
			"reqd" : 1
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
			fieldname: "supervisor",
			label: __("supervisor"),
			fieldtype: "MultiSelectList",
			options: "Supervisor Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Supervisor Master", txt);
			},
			reqd: 0,
		},
        {
			fieldname: "contractor",
			label: __("contractor"),
			fieldtype: "MultiSelectList",
			options: "Supplier",
			get_data: function(txt) {
				return frappe.db.get_link_options("Supplier", txt);
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
        //     "fieldname": "supervisor",
        //     "fieldtype" : "Link",
		// 	"options" : "Supervisor Master",
        //     "label": "Supervisor"
	    // },
        // {
        //     "fieldname": "contractor",
        //     "fieldtype" : "Link",
		// 	"options" : "Supplier",
        //     "label": "Contractor"
	    // },
	]
};
