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
			"fieldtype": "Data",
			"label": "Heat No",
			# "options": "Pouring",
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
			"fieldname": "Contractor_ID",
			"fieldtype": "Link",
			"label": "Contractor ID",
			"options": "Supplier",
		},
				{
			"fieldname": "Contractor_Name",
			"fieldtype": "Link",
			"label": "Contractor Name",
			"options": "Supplier",
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
			"fieldname": "Power_Consumption_per_MT",
			"fieldtype": "Float",
			"label": "Power Consumption per MT",
			# "options": "Item",
			"precision" : "2",
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
			"fieldname": "Raw_Material_Used",
			"fieldtype": "Float",
			"label": "RM Consumed Weight",
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
			"fieldtype": "Float",
			"label": "Good Casting Weight",
		},
		{
			"fieldname": "Burning_Loss_Weight",
			"fieldtype": "Float",
			"label": "Burning Loss Weight",
			# "options": "Item",
		},
		{
			"fieldname": "Percentage_Burning_Loss",
			"fieldtype": "Float",
			"label": "Percentage Burning Loss",
			# "options": "Item",
		},
		{
			"fieldname": "Heat_Count",
			"fieldtype": "Float",
			"label": "Heat Count",
			# "options": "Item",
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
	Operator_ID = filters.get('Operator_ID')
	supervisor_name =  filters.get('supervisor_name')
	Casting_Item_Code =  filters.get('Casting_Item_Code')
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
					p.contractor 'Contractor_ID',
					p.contractor_name 'Contractor_Name',
					p.shift 'Shift',
					((p.power_consumed * c.total_weight)/p.total_pouring_weight) 'Power_Consumed',
					(((p.power_consumed * c.total_weight)/p.total_pouring_weight)/(SUM(c.total_weight)/1000)) "Power_Consumption_per_MT",
					SUM((SELECT SUM(d.poured_boxes)FROM `tabPattern Details` d WHERE p.name = d.parent)) AS 'Poured_Boxes',
					SUM(c.quantitybox) 'Box_Quantity',
					SUM(c.short_quantity) 'Short_Quantity',
					SUM(c.total_quantity) 'Total_Quantity',
					((p.total_consumed_weight * c.total_weight)/p.total_pouring_weight) 'Raw_Material_Used',  
					SUM(c.total_weight) 'Total_Weight',
					SUM(c.rr_weight_total) 'RR_Weight_For_Total_Quantity',
					SUM(c.total_weight)- SUM(c.rr_weight_total) 'Good_Casting_Weight',
					((p.normal_loss * c.total_weight)/p.total_pouring_weight) 'Burning_Loss_Weight',
					(((p.normal_loss * c.total_weight)/p.total_pouring_weight) / SUM(c.total_weight)) * 100 "Percentage_Burning_Loss",
					COUNT(p.name) 'Heat_Count',
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

	if Operator_ID:
		conditions.append("p.operator in %s")
		params.append(Operator_ID)

	if supervisor_name:
		conditions.append("p.supervisor_name = %s")
		params.append(supervisor_name)

	if Casting_Item_Code:
		conditions.append("c.item_code in %s")
		params.append(Casting_Item_Code)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY p.name,p.heat_date ,p.heat_no ,c.item_code ,c.item_name, p.supervisor, p.supervisor_name, p.operator, p.operator_name, p.shift """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data