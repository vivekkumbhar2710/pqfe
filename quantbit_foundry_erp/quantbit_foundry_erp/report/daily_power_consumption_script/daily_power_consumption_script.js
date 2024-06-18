// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Power Consumption Script"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			
		},
		{
			fieldname: "from_date",
			fieldtype: "Date",
			label: "From Date",
			default:'Today',
			reqd: 1,
		},
		{
			fieldname: "to_date",
			fieldtype: "Date",
			label: "To Date",
			default:'Today',
			reqd: 1,
		},
		{
			fieldname: "furnece",
			label: __("Furnece"),
			fieldtype: "MultiSelectList",
			options: "Furnece Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Furnece Master", txt);
			},
			
		},
		{
			fieldname: "Operator_ID",
			label: __("Operator Name"),
			fieldtype: "MultiSelectList",
			options: "Operator Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Operator Master", txt);
			},
			reqd: 0,
		},
		{
			fieldname: "Supervisor_ID",
			label: __("Supervisor Name"),
			fieldtype: "MultiSelectList",
			options: "Supervisor Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Supervisor Master", txt);
			},
			reqd: 0,
		},
		// {
		// 	fieldname: "furnece",
		// 	fieldtype: "Link",
		// 	label: "Furnace",
		// 	options: "Furnece Master",	
		// },
		// {
		// 	fieldname: "Operator_ID",
		// 	fieldtype: "Link",
		// 	label: "Operator Name",
		// 	options: "Operator Master",
		// },
		// {
		// 	fieldname: "Supervisor_ID",
		// 	fieldtype: "Link",
		// 	label: "Supervisor Name",
		// 	options: "Supervisor Master",
		// },
	]
};
