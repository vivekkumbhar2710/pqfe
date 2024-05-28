// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Challan Wise Casting Jobwork out"] = {
	"filters": [
		{
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company",
			"reqd": 1
        },
        {
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
			"reqd": 1
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
			"reqd": 1
        },
		{
			"fieldname": "Out Challan No","fieldtype": "Data","label": "Out Challan No"
		},
        {
            "fieldname": "include_weight",
            "fieldtype": "Check",
            "label": "Include Weight",
        },
	]
};
