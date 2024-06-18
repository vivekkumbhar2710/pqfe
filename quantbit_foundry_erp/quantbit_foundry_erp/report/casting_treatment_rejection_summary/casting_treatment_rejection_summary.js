// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Casting Treatment Rejection Summary"] = {
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
			fieldname: "Rejection_Reason",
			label: __("Rejection Reason"),
			fieldtype: "MultiSelectList",
			options: "Rejection Reason Master",
			get_data: function(txt) {
				return frappe.db.get_link_options("Rejection Reason Master", txt);
			},
			reqd: 0,
		},
		{
			fieldname: "Finished_Item_Code",
			label: __("Finished Item Code"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
			reqd: 0,
		},
		// {
		// 	fieldname: "Rejection_Reason",
		// 	fieldtype: "Link",
		// 	label: "Rejection Reason",
		// 	options: "Rejection Reason Master",
		// },
		// {
		// 	fieldname: "Finished_Item_Code",
		// 	fieldtype: "Link",
		// 	label: "Finished Item Code",
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
