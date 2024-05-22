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
			"fieldname": "name",
			"fieldtype": "Link",
			"label": "ID",
			"options": "Casting Treatment",
		},
		{
			"fieldname": "Casting_Treatment",
			"fieldtype": "Link",
			"label": "Casting Treatment",
			"options": "Casting Treatment",
		},
		# {
		# 	"fieldname": "Heat_No.",
		# 	"fieldtype": "Link",
		# 	"label": "Heat No",
		# 	"options": "Pouring",
			
		# },
		{
			"fieldname": "Operator_ID",
			"fieldtype": "Link",
			"label": "Operator_ID",
			"options": "Operator Master",
		},
		{
			"fieldname": "Operator_Name",
			"fieldtype": "Link",
			"label": "Operator Name",
			"options": "Operator Master",
		},		
		{
			"fieldname": "Supervisor_ID",
			"fieldtype": "Link",
			"label": "Supervisor_ID",
			"options": "Supervisor Master",
		},
				{
			"fieldname": "Supervisor_Name",
			"fieldtype": "Link",
			"label": "Supervisor Name",
			"options": "Supervisor Master",
		},
		# {
		# 	"fieldname": "Shift",
		# 	"fieldtype": "Link",
		# 	"label": "Shift",
		# 	"options": "Shift Master",
		# },
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
		# {
		# 	"fieldname": "Box_Quantity",
		# 	"fieldtype": "Float",
		# 	"label": "Box Quantity",
		# },
		# {
		# 	"fieldname": "Short Quantity",
		# 	"fieldtype": "Float",
		# 	"label": "Short Quantity",
		# 	# "options": "Item",
		# },				
		# {
		# 	"fieldname": "Total_Quantity",
		# 	"fieldtype": "Link",
		# 	"label": "Total_Quantity",
		# 	"options": "Casting Details",
		# },
		# {
		# 	"fieldname": "Total_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "Total Weight",
		# },
		# {
		# 	"fieldname": "RR_Weight_For_Total_Quantity",
		# 	"fieldtype": "Float",
		# 	"label": "RR Weight For Total Quantity",
		# },
		# {
		# 	"fieldname": "Good_Casting_Weight",
		# 	"fieldtype": "float",
		# 	"label": "Good Casting Weight",
		# },
		# {
		# 	"fieldname": "Company",
		# 	"fieldtype": "Link",
		# 	"label": "Company",
		# 	"options": "Company",
		# },
		{
			"fieldname": "OK_Quantity",
			"fieldtype": "Float",
			"label": "OK Quantity",
			# "options": "Item",
		},
		{
			"fieldname": "OK_Quantity_Weight",
			"fieldtype": "Float",
			"label": "OK_Quantity_Weight",
		},		
		{
			"fieldname": "CR_Quantity",
			"fieldtype": "Float",
			"label": "CR Quantity",
			# "options": "Item",
		},		
		{
			"fieldname": "CR_Quantity_Weight",
			"fieldtype": "Float",
			"label": "CR Quantity Weight",
		},
		{
			"fieldname": "RW_Quantity",
			"fieldtype": "Float",
			"label": "RW Quantity",
			# "options": "Item",
		},
		{
			"fieldname": "RW Quantity Weight",
			"fieldtype": "Float",
			"label": "RW Quantity Weight",
		},
		{
			"fieldname": "FR_Quantity",
			"fieldtype": "Float",
			"label": "FR Quantity",
			# "options": "Item",
		},
		{
			"fieldname": "FR_Quantity_Weight",
			"fieldtype": "Float",
			"label": "FR Quantity Weight",
		},		
		{
			"fieldname": "Total_Quantity",
			"fieldtype": "float",
			"label": "Total Quantity",
		},
		{
			"fieldname": "Total_Quantity_Weight",
			"fieldtype": "Float",
			"label": "Total Quantity Weight",
		},				
		# {
		# 	"fieldname": "Supervisor_ID",
		# 	"fieldtype": "float",
		# 	"label": "Supervisor ID",
		# },
		# {
		# 	"fieldname": "Finished_Item",
		# 	"fieldtype": "float",
		# 	"label": "Finished Item",
		# },
		# {
		# 	"fieldname": "Company",
		# 	"fieldtype": "float",
		# 	"label": "Company",
		# },
	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	operator_name = filters.get('operator_name')
	supervisor_name =  filters.get('supervisor_name')
	Casting_Treatment =  filters.get('Casting_Treatment')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
				SELECT 
					c.name,
					c.casting_treatment 'Casting_Treatment',
					c.operator 'Operator_ID',
					c.operator_name 'Operator_Name',
					c.supervisor 'Supervisor_ID',
					c.supervisor_name 'Supervisor_Name',
					q.item_code 'Item_Code',
					q.item_name 'Item_Name',
					SUM(q.ok_quantity) 'OK_Quantity',
					SUM(q.ok_quantity_weight) 'OK_Quantity_Weight',
					SUM(q.cr_quantity) 'CR_Quantity',
					SUM(q.cr_quantity_weight) 'CR_Quantity_Weight',
					SUM(q.rw_quantity) 'RW_Quantiry',
					SUM(q.rw_quantiry_weight) 'RW_Quantiry_Weight',
					SUM(q.fr_quantity) 'FR_Quantity',
					SUM(q.fr_quantity_weight) 'FR_Quantity_Weight',
					SUM(q.total_quantity) 'Total_Quantity',
					SUM(q.weight) 'Total_Quantity_Weight'
				FROM
					`tabCasting Treatment` c
				LEFT JOIN
					`tabCasting Treatment Quantity Details` q ON c.name = q.parent
				WHERE
					casting_treatment = 'FETTLING'
					AND c.docstatus ='1'
					AND c.treatment_date BETWEEN %s AND %s
					AND c.company = %s
				
				"""


	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)
	
	if operator_name:
		conditions.append("c.operator_name = %s")
		params["operator_name"] = operator_name

	if supervisor_name:
		conditions.append("c.supervisor_name = %s")
		params.append(supervisor_name)

	if Casting_Treatment:
		conditions.append("c.casting_treatment = %s")
		params.append(Casting_Treatment)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY c.name, c.casting_treatment, c.operator, c.operator_name, c.supervisor, c.supervisor_name, q.item_code, q.item_name
	  			Having 
					(SUM(q.ok_quantity)+SUM(q.cr_quantity)+SUM(q.rw_quantity)+SUM(q.fr_quantity)) > '0'"""

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data	