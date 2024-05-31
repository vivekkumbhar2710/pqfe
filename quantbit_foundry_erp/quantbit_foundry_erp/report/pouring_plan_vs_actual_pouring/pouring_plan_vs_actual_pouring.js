// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pouring Plan vs Actual Pouring"] = {
	"filters": [
		{
			"label": "Company",
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
			"reqd": 1

		},

		{
			"label": "Month",
			"fieldname": "month",
			"fieldtype": "Select",
			"options": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			"width": 150,
			"reqd": 1
		},
		{
			"label": "Year",
			"fieldname": "year",
			"fieldtype": "Select",
			"options": ["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"],
			"width": 150,
			"reqd": 1
		},

		{
			"label": "Item",
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		
		},

	],
	
        
    
};
	
	
