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
            "fieldname": "supervisor",
            "fieldtype" : "Link",
			"options" : "Supervisor Master",
            "label": "Supervisor"
	    },
        {
            "fieldname": "contractor",
            "fieldtype" : "Link",
			"options" : "Supplier",
            "label": "Contractor"
	    },
	]
};
