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
			"fieldname": "Finished_Item_Code",
			"fieldtype": "Link",
			"label": "Finished Item Code",
			"options": "Item",
		},
		{
			"fieldname": "Finished_Item_Name",
			"fieldtype": "Link",
			"label": "Finished Item Name",
			"options": "Item",
		},		
		{
			"fieldname": "Rejection_Reason",
			"fieldtype": "Link",
			"label": "Rejection Reason",
			"options": "Rejection Reason Master",
		},
		{
			"fieldname": "Rejection_Type",
			"fieldtype": "Link",
			"label": "Rejection Type",
			"options": "Rejection Type Master",
			# "precision" : "2",
		},
		{
			"fieldname": "Qty",
			"fieldtype": "Float",
			"label": "Qty",
			# "options": "Rejection Reason Master",
		},
		{
			"fieldname": "Weight",
			"fieldtype": "Float",
			"label": "Weight",
			# "options": "Rejection Reason Master",
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
	# Operator_Name = filters.get('Operator_Name')
	Finished_Item_Code =  filters.get('Finished_Item_Code')
	Rejection_Reason =  filters.get('Rejection_Reason')
	company =  filters.get('Company')
	conditions = []
	params = [company, from_date, to_date]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
				SELECT 
					i.item_code 'Finished_Item_Code',
					i.item_name 'Finished_Item_Name',
					i.rejection_reason 'Rejection_Reason',
					i.rejection_type 'Rejection_Type',
					SUM(i.qty) 'Qty',
					SUM(i.total_weight) 'Weight',
					c.company 'Company'
				FROM
					`tabCasting Treatment Rejected Items Reasons` i
				LEFT JOIN
					`tabCasting Treatment` c ON i.parent = c.name
				WHERE
					c.docstatus = 1
					AND c.company = %s
					AND c.treatment_date BETWEEN %s AND %s
						
				"""

	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	# if Operator_Name:
	# 	conditions.append("p.operator = %s")
	# 	params.append(Operator_Name)

	if Finished_Item_Code:
		conditions.append("i.item_code in %s")
		params.append(Finished_Item_Code)

	if Rejection_Reason:
		conditions.append("i.rejection_reason in %s")
		params.append(Rejection_Reason)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY i.item_code, i.item_name, i.rejection_reason,	i.rejection_type
				 """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data