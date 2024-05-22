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
			"fieldname": "ID",
			"fieldtype": "Link",
			"label": "ID",
			"options": "Pouring",
		},
		{
			"fieldname": "Heat_Date",
			"fieldtype": "Date",
			"label": "Date",
			# "options": "Pouring",
		},
		{
			"fieldname": "Heat_No.",
			"fieldtype": "Link",
			"label": "Heat No",
			"options": "Pouring",
		},
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
		{
			"fieldname": "Shift",
			"fieldtype": "Link",
			"label": "Shift",
			"options": "Shift Master",
		},
		{
			"fieldname": "Casting_Item_Code",
			"fieldtype": "Link",
			"label": "Casting Item Code",
			"options": "Casting Details",
		},
		{
			"fieldname": "Casting_Item_Name",
			"fieldtype": "Link",
			"label": "Casting Item Name",
			"options": "Casting Details",
		},		
		{
			"fieldname": "Power_Consumed",
			"fieldtype": "Float",
			"label": "Power Consumed",
			# "options": "Item",
		},
		{
			"fieldname": "Burning_Loss_Weight",
			"fieldtype": "Float",
			"label": "Burning Loss Weight",
			# "options": "Item",
		},
		{
			"fieldname": "Poured_Boxes",
			"fieldtype": "Float",
			"label": "Poured Boxes",
			# "options": "Item",
		},						
		{
			"fieldname": "Box_Quantity",
			"fieldtype": "Float",
			"label": "Box Quantity",
		},
		{
			"fieldname": "Short Quantity",
			"fieldtype": "Float",
			"label": "Short Quantity",
			# "options": "Item",
		},				
		{
			"fieldname": "Total_Quantity",
			"fieldtype": "Link",
			"label": "Total_Quantity",
			"options": "Casting Details",
		},
		{
			"fieldname": "Total_Weight",
			"fieldtype": "Float",
			"label": "Total Weight",
		},
		{
			"fieldname": "RR_Weight_For_Total_Quantity",
			"fieldtype": "Float",
			"label": "RR Weight For Total Quantity",
		},
		{
			"fieldname": "Good_Casting_Weight",
			"fieldtype": "float",
			"label": "Good Casting Weight",
		},
		{
			"fieldname": "Company",
			"fieldtype": "Link",
			"label": "Company",
			"options": "Company",
			
		},
		# {
		# 	"fieldname": "CR_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "CR Weight",
		# },
		# {
		# 	"fieldname": "MR_QTY",
		# 	"fieldtype": "Float",
		# 	"label": "MR QTY",
		# 	# "options": "Item",
		# },
		# {
		# 	"fieldname": "MR_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "MR Weight",
		# },
		# {
		# 	"fieldname": "RW_QTY",
		# 	"fieldtype": "Float",
		# 	"label": "RW QTY",
		# 	# "options": "Item",
		# },
		# {
		# 	"fieldname": "RW_Weight",
		# 	"fieldtype": "Float",
		# 	"label": "RW Weight",
		# },
		# {
		# 	"fieldname": "Total_QTY",
		# 	"fieldtype": "float",
		# 	"label": "Total QTY",
		# },		
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
	Casting_Item_Name =  filters.get('Casting_Item_Name')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
				Select
					#case when c.item_code is null then 'Missing Item' else c.item_code end AS 'Blank',
					p.name 'ID',
					p.heat_date 'Heat_Date',
					p.heat_no 'Heat_No.',
					c.item_code 'Casting_Item_Code',
					c.item_name 'Casting_Item_Name',
					p.supervisor 'Supervisor_ID',
					p.supervisor_name 'Supervisor_Name',
					p.operator 'Operator_ID',
					p.operator_name 'Operator_Name',
					p.shift 'Shift',
					SUM(p.power_consumed) 'Power_Consumed',
					SUM(p.normal_loss) 'Burning_Loss_Weight',
					SUM((SELECT SUM(d.poured_boxes)FROM `tabPattern Details` d WHERE p.name = d.parent)) AS 'Poured_Boxes',
					SUM(c.quantitybox) 'Box_Quantity',
					SUM(c.short_quantity) 'Short_Quantity',
					SUM(c.total_quantity) 'Total_Quantity',
					#SUM(p.total_consumed_weight) 'Raw_Material_Used',
					SUM(c.total_weight) 'Total_Weight',
					SUM(c.rr_weight_total) 'RR_Weight_For_Total_Quantity',
					SUM(c.total_weight)- SUM(c.rr_weight_total) 'Good_Casting_Weight',
					p.company 'Company'
				FROM
					`tabPouring` p
				LEFT JOIN
					`tabCasting Details` c ON p.name = c.parent
				WHERE
					p.docstatus = '1'
					AND p.heat_date BETWEEN %s AND %s
					AND p.company = %s
				
					
				"""


	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	if operator_name:
		conditions.append("p.operator_name = %s")
		params["operator_name"] = operator_name

	if supervisor_name:
		conditions.append("p.supervisor_name = %s")
		params.append(supervisor_name)

	if Casting_Item_Name:
		conditions.append("c.item_name = %s")
		params.append(Casting_Item_Name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY p.name,p.heat_date ,p.heat_no ,c.item_code ,c.item_name, p.supervisor, p.supervisor_name, p.operator, p.operator_name, p.shift """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data