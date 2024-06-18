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
			"fieldname": "Item_Code",
			"fieldtype": "Link",
			"label": "Item Code",
			"options": "Item",
		},
		{
			"fieldname": "Item_Name",
			"fieldtype": "Link",
			"label": "Item Name",
			"options": "Item",
		},
		{
			"fieldname": "Total_Quantity",
			"fieldtype": "Float",
			"label": "Total Quantity",
			# "options": "Pouring",
		},
		{
			"fieldname": "RR_Weight_For_Total_Quantity",
			"fieldtype": "Float",
			"label": "RR Weight For Total Quantity",
			# "options": "",
		},
		{
			"fieldname": "Total_Weight",
			"fieldtype": "Float",
			"label": "Total Weight",
			# "options": "",
		},		
		{
			"fieldname": "Good_Casting_Weight",
			"fieldtype": "Float",
			"label": "Good Casting Weight",
			# "options": "",
		},
		{
			"fieldname": "Poured_Boxes",
			"fieldtype": "Float",
			"label": "Poured_Boxes",
			# "options": "",
		},
		{
			"fieldname": "Grade_Type",
			"fieldtype": "Link",
			"label": "Grade Type",
			"options": "Grade Type",
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
	Item_Code = filters.get('Item_Code')
	# supervisor_name =  filters.get('supervisor_name')
	# Casting_Item_Name =  filters.get('Casting_Item_Name')
	company =  filters.get('Company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}
	# frappe.throw(str(item_code))


	sql_query = """
				SELECT 
				c.item_code 'Item_Code',
				c.item_name 'Item_Name',
				SUM(c.total_quantity) 'Total_Quantity',
				SUM(c.rr_weight_total) 'RR_Weight_For_Total_Quantity',
				SUM(c.total_weight) 'Total_Weight',
				SUM(c.total_weight) - SUM(c.rr_weight_total) 'Good_Casting_Weight',
				SUM(pd.poured_boxes) 'Poured_Boxes',
				p.grade_type 'Grade_Type',
				p.company 'Company'
			FROM
				`tabPouring` p
			LEFT JOIN
				`tabCasting Details` c ON p.name = c.parent
			LEFT JOIN
				`tabPattern Details` pd ON p.name = pd.parent
			WHERE
				p.docstatus = '1'
				AND p.heat_date BETWEEN %s AND %s
				AND p.company = %s
				# AND c.item_code IS NOT NULL		
				"""
	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	if Item_Code:
		conditions.append("c.item_code in %s")
		params.append(Item_Code)

	# if supervisor_name:
	# 	conditions.append("p.supervisor_name = %s")
	# 	params.append(supervisor_name)

	# if Casting_Item_Name:
	# 	conditions.append("c.item_code = %s")
	# 	params.append(Casting_Item_Name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY c.item_code, c.item_name, p.grade_type, p.company """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data