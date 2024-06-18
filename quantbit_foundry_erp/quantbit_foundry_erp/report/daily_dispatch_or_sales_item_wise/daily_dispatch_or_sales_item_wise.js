// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Dispatch OR Sales Item-wise"] = {
	"filters": [
		{
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company"
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
			fieldname: "item_code",
			label: __("Item Name"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
        // {
        //     "fieldname": "item_code",
        //     "fieldtype": "Link",
        //     "label": "Item Name",
        //     "options": "Item"
        // }
	]
};
