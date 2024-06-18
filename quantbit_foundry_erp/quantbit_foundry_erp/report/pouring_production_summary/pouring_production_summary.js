// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pouring Production Summary"] = {
	"filters": [
		{
			fieldname: "Company",
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
			fieldname: "Item_Code",
			label: __("Item Name"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
		// {
		// 	fieldname: "Item_Code",
		// 	fieldtype: "Link",
		// 	label: "Item Code",
		// 	options: "Item",
		// },
		// {
		// 	fieldname: "Operator_Name",
		// 	fieldtype: "Link",
		// 	label: "Operator Name",
		// 	options: "Operator Master",
			
		// },
		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
