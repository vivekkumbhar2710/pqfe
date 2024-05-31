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
			"fieldname" : "stock_entry_type",
			"fieldtype" : "Data",
			"label" : "Stock Entry Type"
		},
		{
			"fieldname" : "item_group",
			"fieldtype" : "Data",
			"label" : "Item Group",
			"width":180
		},
		{
			"fieldname" : "item_code",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Item Code",
			"width":280
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
			"label" : "Quantity",
			"precision": 3,
			"width":150
		},
		{
			"fieldname" : "valuation_rate",
			"fieldtype" : "Float",
			"label" : "Item Rate",
			"precision": 3,
			"width":150
		},
		{
			"fieldname" : "amount",
			"fieldtype" : "Float",
			"label" : "Amount",
			"precision": 3,
			"width":150
		},
		{
			"fieldname" : "department",
			"fieldtype" : "Data",
			"label" : "Source Department"			
		},
		{
			"fieldname" : "machine",
			"fieldtype" : "Data",
			"label" : "Source Machine"			
		},
		{
			"fieldname" : "operation",
			"fieldtype" : "Data",
			"label" : "Source Operation"			
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
	item_group = filters.get("item_group")
	stock_entry_type = filters.get("stock_entry_type")
	stock_entry_type = filters.get("stock_entry_type")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
						se.stock_entry_type AS "stock_entry_type",
	 					sed.item_group AS "item_group", 
						sed.item_code AS "item_code",
						sed.item_name AS "item_name",
						ROUND(SUM(sed.qty), 2) AS "qty",
						ROUND(AVG(sed.valuation_rate), 2) AS "valuation_rate",
						ROUND(SUM(sed.amount), 2) AS "amount",
						sed.department AS "department",
						sed.machine AS "machine",
						sed.operation AS "operation",
						se.company AS "company"
					FROM 
						`tabStock Entry` se
					LEFT JOIN 
						`tabStock Entry Detail` sed ON se.name = sed.parent
					WHERE
						se.company = %s AND DATE(se.posting_date) BETWEEN %s AND %s AND se.docstatus = 1
						AND (se.stock_entry_type = 'Material Issue' OR se.stock_entry_type = 'Manufacture')
						AND sed.is_finished_item = 0 					
                        """
    
	if item_group:
		add_condition(conditions, params, "sed.item_group = %s", item_group)
	if stock_entry_type:
		add_condition(conditions, params, "se.stock_entry_type = %s", stock_entry_type)
		
	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY sed.item_code, sed.department, sed.machine, sed.operation"

	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data
 
