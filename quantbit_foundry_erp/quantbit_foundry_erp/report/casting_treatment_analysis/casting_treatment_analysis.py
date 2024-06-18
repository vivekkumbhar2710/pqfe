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
			"fieldname" : "name",
			"fieldtype" : "Link",
			"options" : "Casting Treatment",
			"label" : "Id",
			"width":100
		},
		{
			"fieldname" : "treatment_date",
			"fieldtype" : "Date",
			"label" : "Treatment Date"
		},
		{
			"fieldname" : "casting_treatment",
			"fieldtype" : "Data",
			"label" : "Casting Treatment"
		},
		{
			"fieldname" : "contractor",
			"fieldtype" : "Link",
			"options" : "Supplier",
			"label" : "Contractor Id"
		},
		{
			"fieldname" : "contractor_name",
			"fieldtype" : "Data",
			"label" : "Contractor Name"
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
			"fieldname" : "quantity",
			"fieldtype" : "Float",
			"label" : "Quantity",
			"width":150,
			"precision": 3
		},
		
		{
			"fieldname" : "weight",
			"fieldtype" : "Float",
			"label" : "Weight",
			"width":150,
			"precision": 3
		},
		{
			"fieldname" : "source_warehouse",
			"fieldtype" : "Data",
			"label" : "Source Warehouse"
		},
		{
			"fieldname" : "target_warehouse",
			"fieldtype" : "Data",
			"label" : "Target Warehouse"
		},
		{
			"fieldname" : "company",
			"fieldtype" : "Data",
			"label" : "Company"
		}
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
	contractor = filters.get("contractor")
	casting_treatment = filters.get("casting_treatment")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT
						ct.name AS 'name', 
						ct.treatment_date AS 'treatment_date', 
						ct.casting_treatment AS 'casting_treatment', 
						#sum_of_total_quantity AS 'Total Quantity', 
						#sum_of_total_weight AS 'Total Weight', 
						ct.contractor AS 'contractor', 
						ct.contractor_name AS 'contractor_name',
						pc.item_code AS 'item_code',
						pc.item_name AS 'item_name',
						SUM(pc.quantity) AS 'quantity',
						SUM(pc.weight) AS 'weight',
						pc.source_warehouse AS 'source_warehouse',
						pc.target_warehouse AS 'target_warehouse',
						ct.company AS 'company'
					FROM 
						`tabCasting Treatment`ct
					INNER JOIN 
						`tabCasting Treatment Pattern Casting Item` pc ON ct.name = pc.parent
					WHERE
						ct.company = %s AND DATE(ct.treatment_date) BETWEEN %s AND %s AND ct.docstatus = 1
						
						
                """
	if item:
		add_condition(conditions, params, "pc.item_code in %s", item) 

	if contractor:
		add_condition(conditions, params, "ct.contractor in %s", contractor)
	
	if casting_treatment:
		add_condition(conditions, params, "ct.casting_treatment in %s", casting_treatment)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)
	
	sql_query += " GROUP BY ct.name, ct.treatment_date, ct.casting_treatment,  ct.contractor, ct.contractor_name, pc.item_code, pc.item_name, pc.source_warehouse, pc.target_warehouse, ct.company"
	    
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data

	