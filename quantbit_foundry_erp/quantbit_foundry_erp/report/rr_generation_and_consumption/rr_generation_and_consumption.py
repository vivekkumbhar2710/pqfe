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
			"fieldtype" : "Data",
			"label" : "Document Id"
		},
		{
			"fieldname" : "heat_no",
			"fieldtype" : "Data",
			"label" : "Heat Number"
		},
		{
			"fieldname" : "pattern_name",
			"fieldtype" : "Data",
			"label" : "Pattern Name",
			"width": 350
		},
		{
			"fieldname" : "item_code",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Retained Item Code"
		},
		{
			"fieldname" : "item_name",
			"fieldtype" : "Data",
			"label" : "Retained Item Name"
		},
		{
			"fieldname" : "total_quantity",
			"fieldtype" : "Float",
			"label" : "Generated Weight",
			"precision": 3
		},
		{
			"fieldname" : "item_code",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Consumed Item Code"
		},
		{
			"fieldname" : "item_name",
			"fieldtype" : "Data",
			"label" : "Consumed Item Name"
		},
		{
			"fieldname" : "quantity",
			"fieldtype" : "Float",
			"label" : "Consumed Weight",
			"precision": 3
		},
		{
			"fieldname" : "supervisor",
			"fieldtype" : "Link",
			"options" : "Supervisor Master",
			"label" : "Supervisor Id"
		},
		{
			"fieldname" : "supervisor_name",
			"fieldtype" : "Data",
			"label" : "Supervisor Name",
			"width": 200
		},
		{
			"fieldname" : "operator",
			"fieldtype" : "Link",
			"options" : "Operator Master",
			"label" : "Operator Id"
		},
		{
			"fieldname" : "operator_name",
			"fieldtype" : "Data",
			"label" : "Operator Name",
			"width": 200
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
	sup_name = filters.get("supervisor")
	operator_name = filters.get("operator")
	contractor_name = filters.get("contractor")
	item_code = filters.get("item_code")
	heat_no = filters.get("heat_no")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
					p.name AS "name", p.heat_no 'heat_no', pd.pattern_name 'pattern_name',	r.item_code 'item_code',
					r.item_name 'item_name', SUM(r.total_quantity) 'total_quantity', cmd.item_code 'item_code',
					cmd.item_name 'item_name', cmd.quantity 'quantity', p.supervisor 'supervisor', p.supervisor_name 'supervisor_name',
					p.operator 'operator', p.operator_name 'operator_name',	p.contractor 'contractor', p.contractor_name 'contractor_name',
					p.company
					FROM
						`tabPouring` p
					INNER JOIN
						`tabRetained Items` r ON p.name = r.parent
					Left JOIN 
						`tabChange Mix Details` cmd on r.item_code = cmd.item_code and r.parent= cmd.parent
					INNER JOIN
						`tabPattern Details` pd ON p.name = pd.parent
					WHERE
						p.company = %s AND DATE(p.heat_date) BETWEEN %s AND %s AND p.docstatus = 1
					"""
    
	if sup_name:
		add_condition(conditions, params, "p.supervisor in %s", sup_name)
	if operator_name:
		add_condition(conditions, params, "p.operator in %s", operator_name)
	if contractor_name:
		add_condition(conditions, params, "p.contractor in %s", contractor_name)
	if item_code:
		add_condition(conditions, params, "cmd.item_code in %s", item_code) 
	if heat_no:
		add_condition(conditions, params, "p.heat_no = %s", heat_no)
		 
	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY p.name, p.heat_no, pd.pattern_name, r.item_code, r.item_name, cmd.item_code,cmd.item_name, cmd.quantity, p.supervisor, p.supervisor_name, p.operator,p.operator_name, p.company"

	# frappe.throw(str(sql_query))

	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data