# Copyright (c) 2024, quantdairy and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data


def get_columns(filters):
	return [
		{
			"fieldname": "Raw_Item_Code",
			"fieldtype": "Link",
			"label": "Raw Item Code",
			"options": "Item",
		},
		{
			"fieldname": "Raw_Item_Name",
			"fieldtype": "Link",
			"label": "Raw Item Name",
			"options": "Item",
		},
		{
			"fieldname": "Used_Quantity",
			"fieldtype": "Float",
			"label": "Used Quantity",
			# "options": "",
		},		
		{
			"fieldname": "Company",
			"fieldtype": "Link",
			"label": "Company",
			"options": "Company",
		},
		
	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	Raw_Item_Code = filters.get('Raw_Item_Code')
	# Core_Item_Code =  filters.get('Core_Item_Code')
	# Casting_Item_Name =  filters.get('Casting_Item_Name')
	company =  filters.get('Company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}
	# frappe.throw(str(item_code))


	sql_query = """
				Select
					c.item_code 'Raw_Item_Code',
					c.item_name 'Raw_Item_Name',
					SUM(c.quantity) 'Used_Quantity',
					p.grade_type 'Grade_Type',
					p.company 'Company'
				FROM
					`tabChange Mix Details` c
				LEFT JOIN
					`tabPouring` p ON c.parent = p.name
				WHERE
					p.docstatus = 1
					AND p.heat_date BETWEEN %s AND %s
					AND p.company = %s
				
				

				"""
	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	if Raw_Item_Code:
		conditions.append("c.item_code in %s")
		params.append(Raw_Item_Code)

	# if Core_Item_Code:
	# 	conditions.append("c.item_code = %s")
	# 	params.append(Core_Item_Code)

	# if Casting_Item_Name:
	# 	conditions.append("c.item_code = %s")
	# 	params.append(Casting_Item_Name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY 
					c.item_code,
					c.item_name,
					p.company
				"""

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data