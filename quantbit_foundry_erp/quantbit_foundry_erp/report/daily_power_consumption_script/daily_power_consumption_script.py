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
			"fieldname": "Heat_Date",
			"fieldtype": "Date",
			"label": "Heat Date",
			# "options": "Casting Treatment",
		},
		{
			"fieldname": "Furnace",
			"fieldtype": "Link",
			"label": "Furnace",
			"options": "Furnece Master",
		},
		{
			"fieldname": "Operator_Name",
			"fieldtype": "Link",
			"label": "Operator Name",
			"options": "Operator Master",
		},
		{
			"fieldname": "Supervisor_Name",
			"fieldtype": "Link",
			"label": "Supervisor Name",
			"options": "Supervisor Master",
		},
		{
			"fieldname": "Heat_Count",
			"fieldtype": "Data",
			"label": "Heat Count",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Burning_Loss_Weight",
			"fieldtype": "Float",
			"label": "Burning Loss Weight",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Total_pouring_weight",
			"fieldtype": "Float",
			"label": "Total pouring weight",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Percentage_Burning_Loss",
			"fieldtype": "Float",
			"label": "Percentage Burning Loss",
			# "options": "Pouring",
			
		},								
		{
			"fieldname": "Power_Consumed",
			"fieldtype": "Data",
			"label": "Power Consumed",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Power_Consumption_per_MT",
			"fieldtype": "Float",
			"label": "Power Consumption per MT",
			# "options": "Pouring",
			"precision" : "2",			
		},		
		{
			"fieldname": "Operator_ID",
			"fieldtype": "Link",
			"label": "Operator ID",
			"options": "Operator Master",
		},
		{
			"fieldname": "Supervisor_ID",
			"fieldtype": "Link",
			"label": "Supervisor ID",
			"options": "Supervisor Master",
		},		
		{
			"fieldname": "Company",
			"fieldtype": "float",
			"label": "Company",
		},

	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	Furnace = filters.get('furnece')
	Operator_Name =  filters.get('Operator_ID')
	Supervisor_Name =  filters.get('Supervisor_ID')
	company =  filters.get('company')
	conditions = []
	params = [from_date, to_date , company]
	# params = [from_date, to_date]
	# params = {"from_date": from_date, "to_date": to_date, "company": "YourCompany"}

	# frappe.throw(str(item_code))


	sql_query = """
				select 
					heat_date "Heat_Date",
					furnece "Furnace",
					operator_name "Operator_Name",
					supervisor_name "Supervisor_Name",
					COUNT(name) AS "Heat_Count",
					SUM(normal_loss) "Burning_Loss_Weight",
					SUM(total_pouring_weight) "Total_pouring_weight",
					(SUM(normal_loss) / SUM(total_pouring_weight)) * 100 "Percentage_Burning_Loss",
					#sum(power_reading_initial) "PowerReading Initial",
					#sum(power_reading_final) "Power Reading Final",
					sum(power_consumed) "Power_Consumed",
					(sum(power_consumed)/(SUM(total_pouring_weight)/1000)) "Power_Consumption_per_MT",
					operator "Operator_ID",
					supervisor "Supervisor_ID",
					company "Company"
				from 
					`tabPouring`
				where
					heat_date between %s and %s 
					and company =%s
								
				"""


	if Furnace:
		conditions.append("furnece in %s")
		params.append(Furnace)
		# params["operator_name"] = operator_name

	if Operator_Name:
		
		conditions.append("operator in %s")
		params.append(Operator_Name)

	if Supervisor_Name:
		conditions.append("supervisor in %s")
		params.append(Supervisor_Name)

	# if Casting_Treatment:
	# 	conditions.append("c.casting_treatment = %s")
	# 	params.append(Casting_Treatment)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY heat_date,furnece,operator,supervisor,company """

	# frappe.throw(str(sql_query)+'======'+str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data