# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data 
 
def get_columns():
	return[
		{
			"fieldname" : "customer",
			"fieldtype" : "Link",
			"options" : "Customer",
			"label" : "Customer"
		},
		{
			"fieldname" : "customer_name",
			"fieldtype" : "Data",
			"label" : "Customer Name",
			"width":300
		},
		{
			"fieldname" : "item_code",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Item Code",
			"width":300
		},
		{
			"fieldname" : "item_name",
			"fieldtype" : "Data",
			"label" : "Item Name",
			"width":280
		},
		{
			"fieldname" : "qty",
			"fieldtype" : "Float",
			"label" : "Quantity (Nos)",
			"precision": 3
		},
		{
			"fieldname" : "value_per_unit",
			"fieldtype" : "Float",
			"label" : "Average Weight (Kg)",
			"precision": 3
		},
		{
			"fieldname" : "total_weight",
			"fieldtype" : "Float",
			"label" : "Total Weight (Kg)",
			"precision": 3
		},
		{
			"fieldname" : "amount",
			"fieldtype" : "Float",
			"label" : "Net Amount",
			"precision": 2,
			"width":150
		},
		{
			"fieldname" : "tax_amount",
			"fieldtype" : "Float",
			"label" : "Tax Amount",
			"precision": 2,
			"width":150
		}, 
		{
			"fieldname" : "total_amount",
			"fieldtype" : "Float",
			"label" : "Total Amount",
			"precision": 2,
			"width":150
		},
		{
			"fieldname" : "company",
			"fieldtype" : "Data",
			"label" : "Company"
		},
	] 


def add_condition(condition_list, params_list, condition, param_value):
    if param_value:
        condition_list.append(condition)
        params_list.append(param_value)

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	comp = filters.get("company")
	item = filters.get("item_code")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT
						dn.customer AS "customer",
						dn.customer_name AS "customer_name",
						dni.item_code AS "item_code",
						dni.item_name AS "item_name",
						ROUND(SUM(dni.qty), 2) AS "qty",
						ROUND(AVG(uom.value_per_unit),2) AS "value_per_unit",
						SUM(dni.qty * uom.value_per_unit) AS "total_weight", 
						ROUND(SUM(dni.amount),2) AS "amount",
						ROUND(SUM(dni.cgst_amount + dni.sgst_amount + dni.igst_amount), 2) AS "tax_amount",
						ROUND(SUM(dni.amount + dni.cgst_amount + dni.sgst_amount + dni.igst_amount), 2) AS "total_amount",
						dn.company AS "company"
					FROM 
						`tabDelivery Note` dn
					INNER JOIN 
						`tabDelivery Note Item` dni ON dn.name = dni.parent
					INNER JOIN
						`tabItem` item ON dni.item_code = item.item_code
						AND item.company = dn.company
					LEFT JOIN
						`tabProduction UOM Definition` uom ON item.name = uom.parent
						AND uom.uom = 'Kg'
					WHERE
						dn.company = %s AND DATE(dn.posting_date) BETWEEN %s AND %s AND dn.docstatus = 1
						AND (dn.custom_job_work_receipt IS NULL OR dn.custom_job_work_receipt = '')
						
                """
	if item:
		add_condition(conditions, params, "dni.item_code= %s", item)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)
	
	sql_query += " GROUP BY dni.item_code, dn.customer_name, dn.company"
	    
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data

	