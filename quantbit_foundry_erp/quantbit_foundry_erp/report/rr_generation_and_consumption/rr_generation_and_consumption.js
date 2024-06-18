// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["RR Generation and Consumption"] = {
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
            "label": __("From Date"),
            "reqd": 1,
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": __("To Date"),
            "reqd": 1,
            "default": frappe.datetime.get_today()
        },
        {
			fieldname: "operator",
			label: __("Opeartor"),
			fieldtype: "MultiSelectList",
			options: "Operator Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Operator Master", txt);
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
        {
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
        {
            "fieldname": "heat_no",
            "fieldtype": "Data",
            "label": "Heat No"
        },
        // {
        //     "fieldname": "supervisor",
        //     "fieldtype" : "Link",
		// 	"options" : "Supervisor Master",
        //     "label": "Supervisor Id"
	    // },
        // {
        //     "fieldname": "operator",
        //     "fieldtype" : "Link",
		// 	"options" : "Operator Master",
        //     "label": "Opeartor Id"
	    // },	
        // {
        //     "fieldname": "contractor",
        //     "fieldtype" : "Link",
		// 	"options" : "Supplier",
        //     "label": "Contractor Id"
	    // },
        // {
        //     "fieldname": "item_code",
        //     "fieldtype" : "Link",
		// 	"options" : "Item",
        //     "label": "Item"
	    // }			
	],

    "onload": function(report) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Pouring",
                fields: ["heat_no"]
            },
            callback: function(response) {
                if (response && response.message) {
                    let heat_no_options = response.message.map(doc => doc.heat_no);
                    let heat_no_field = report.filters_by_name.heat_no;
                    
                    heat_no_field.df.options = heat_no_options;
                    heat_no_field.refresh();
                }
            }
        });
    }

};
