// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Heat Wise Daily Production Script"] = {
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
			fieldname: "Casting_Item_Code",
			label: __("Casting Item Name"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
		// {
		// 	fieldname: "Operator_Name",
		// 	fieldtype: "Link",
		// 	label: "Operator Name",
		// 	options: "Operator Master",
			
		// },
		// {
		// 	fieldname: "Casting_Item_Name",
		// 	fieldtype: "Link",
		// 	label: "Casting Item Name",
		// 	options: "Item",
		// },

		// {
		// 	fieldname: "route",
		// 	fieldtype: "Link",
		// 	label: "Route",
		// 	options: "Route Master",
		// },
	]
};
