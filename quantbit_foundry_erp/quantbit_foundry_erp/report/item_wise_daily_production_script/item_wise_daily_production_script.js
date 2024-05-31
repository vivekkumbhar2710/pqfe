// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item wise Daily Production Script"] = {
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
			fieldname: "operator_name",
			fieldtype: "Link",
			label: "Operator Name",
			options: "Operator Master",
			
		},
		{
			fieldname: "Casting_Item_Code",
			fieldtype: "Link",
			label: "Casting Item Name",
			options: "Item",
		},

		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
