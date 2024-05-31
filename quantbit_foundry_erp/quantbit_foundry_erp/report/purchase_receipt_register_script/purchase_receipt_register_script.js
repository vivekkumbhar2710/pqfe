// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Receipt Register Script"] = {
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
            "fieldname": "item_group",
            "fieldtype" : "Link",
			"options" : "Item Group",
            "label": "Item Group"
	    }
		
	]
};