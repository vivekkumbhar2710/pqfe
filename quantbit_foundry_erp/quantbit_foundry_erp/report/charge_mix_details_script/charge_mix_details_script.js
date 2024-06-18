// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Charge Mix Details Script"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			reqd:1,			
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
			fieldname: "Pouring_Id",
			label: __("Pouring Id"),
			fieldtype: "MultiSelectList",
			options: "Pouring",
			get_data: function(txt) {
				return frappe.db.get_link_options("Pouring", txt);
			},
			reqd: 0,
		},
		// {
		// 	fieldname: "Pouring_Id",
		// 	fieldtype: "Link",
		// 	label: "Pouring Id",
		// 	options: "Pouring",
			
		// },
		{
			fieldname: "Heat_No",
			fieldtype: "Data",
			label: "Heat No",
			options: "Pouring",
		},

		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
