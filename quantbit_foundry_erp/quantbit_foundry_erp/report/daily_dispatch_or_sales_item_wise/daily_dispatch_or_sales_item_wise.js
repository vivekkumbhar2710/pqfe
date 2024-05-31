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
            "label": "From Date"
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date"
        },
        {
            "fieldname": "item_code",
            "fieldtype": "Link",
            "label": "Item Name",
            "options": "Item"
        }
	]
};
