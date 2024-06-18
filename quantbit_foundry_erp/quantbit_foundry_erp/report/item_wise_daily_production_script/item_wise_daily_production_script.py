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
			"fieldname": "Date",
			"fieldtype": "Date",
			"label": "Date",
			# "options": "Pouring",
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
			"fieldname": "Percentage_Burning_Loss",
			"fieldtype": "Float",
			"label": "Percentage Burning Loss",
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
			"label": "RRW Weight For Total Quantity",
			# "options": "Casting Details",
		},
		{
			"fieldname": "Good_Casting_Weight",
			"fieldtype": "Float",
			"label": "Good Casting Weight",
		},
		{
			"fieldname": "Company",
			"fieldtype": "Link",
			"label": "Company",
			"options": "Company",
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
	Operator_ID = filters.get('Operator_ID')
	# operator_name = frappe.get_value('Operator Master' ,operator_id , 'operator_name' )

	# frappe.throw(str(operator_id))
	# supervisor_name =  filters.get('supervisor_name')
	Casting_Item_Name =  filters.get('Casting_Item_Code')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
				Select
					case when c.item_code is null then 'Missing Item' else c.item_code end AS 'Item_Code',
					p.name 'ID',
					p.heat_date 'Date',
					p.supervisor 'Supervisor_ID',
					p.supervisor_name 'Supervisor_Name',
					p.operator 'Operator_ID',
					p.operator_name 'Operator_Name',
					p.shift 'Shift',
					c.item_code 'Casting_Item_Code',
					c.item_name 'Casting_Item_Name',
					((p.power_consumed * c.total_weight)/p.total_pouring_weight) 'Power_Consumed',
    				((p.normal_loss * c.total_weight)/p.total_pouring_weight) 'Burning_Loss_Weight',
					(((p.normal_loss * c.total_weight)/p.total_pouring_weight)/ SUM(c.total_weight)) * 100 "Percentage_Burning_Loss",
    				SUM((SELECT SUM(d.poured_boxes)FROM `tabPattern Details` d WHERE p.name = d.parent)) AS 'Poured_Boxes',
					SUM(c.quantitybox) 'Box_Quantity',
					SUM(c.short_quantity) 'Short_Quantity',
					SUM(c.total_quantity) 'Total_Quantity',
					SUM(c.total_weight) 'Total_Weight',
					SUM(c.rr_weight_total) 'RR_Weight_For_Total_Quantity',
					SUM(c.total_weight)- SUM(c.rr_weight_total) 'Good_Casting_Weight',
					p.company 'Company'
					#(SELECT SUM(c.total_quantity) FROM `tabCasting Details` c WHERE p.name = c.parent) 'Total_Quantity',
					#SUM((SELECT SUM(c.rr_weight_total) FROM `tabCasting Details` c WHERE p.name = c.parent)) 'RR_Weight_For_Total_Quantity'
					#SUM((SELECT SUM(c.total_weight) FROM `tabCasting Details` c WHERE p.name = c.parent)) 'Total_Weight',
					#(SELECT (SUM(c.total_weight)- SUM(c.rr_weight_total)) FROM `tabCasting Details` c WHERE p.name = c.parent) 'Good_Casting'

				FROM
					`tabPouring` p
				LEFT JOIN
					`tabCasting Details` c ON p.name = c.parent
				WHERE
					p.docstatus = '1'
					AND p.heat_date BETWEEN %s AND %s
					AND p.company = %s
				"""




	if Operator_ID:
		conditions.append("p.operator in %s")
		# params["operator_name"] = operator_name
		params.append(Operator_ID)

	# if production_item:
	# 	conditions.append("wo.production_item = %s")
	# 	params.append(production_item)

	# if supervisor_name:
	# 	conditions.append("p.supervisor_name = %s")
	# 	params.append(supervisor_name)

	if Casting_Item_Name:
		conditions.append("c.item_code in %s")
		params.append(Casting_Item_Name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY p.name, p.heat_date, p.company, p.supervisor, p.operator, p.shift, c.item_code """

	# frappe.throw(str(params))
	# frappe.throw(str(sql_query)+'======'+str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data