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
			fieldtype: "Link",
			label: "Furnace",
			options: "Furnece Master",
			
		},
		// {
		// 	fieldname: "Casting_Treatment",
		// 	fieldtype: "Link",
		// 	label: "Casting Treatment",
		// 	options: "Casting Treatment Master",
		// },

		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
