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
			"fieldname": "Heat_Count",
			"fieldtype": "Data",
			"label": "Heat Count",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Burning_Loss_Weight",
			"fieldtype": "Data",
			"label": "Burning Loss Weight",
			# "options": "Pouring",
			
		},
		{
			"fieldname": "Total_pouring_weight",
			"fieldtype": "Data",
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
			"fieldname": "Company",
			"fieldtype": "float",
			"label": "Company",
		},

	]


def get_data(filters):
	
	from_date = filters.get('from_date')
	to_date =  filters.get('to_date')
	Furnace = filters.get('furnece')
	# supervisor_name =  filters.get('supervisor_name')
	# Casting_Treatment =  filters.get('Casting_Treatment')
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
					COUNT(name) AS "Heat_Count",
					SUM(normal_loss) "Burning_Loss_Weight",
					SUM(total_pouring_weight) "Total_pouring_weight",
					(SUM(normal_loss) / SUM(total_pouring_weight)) * 100 "Percentage_Burning_Loss",
					#sum(power_reading_initial) "PowerReading Initial",
					#sum(power_reading_final) "Power Reading Final",
					sum(power_consumed) "Power_Consumed",
					company "Company"
				from 
					`tabPouring`
				where
					heat_date between %s and %s 
					and company =%s
								
				"""


	if Furnace:
		conditions.append("furnece = %s")
		params.append(Furnace)

	# if operator_name:
	# 	conditions.append("c.operator_name = %s")
	# 	params["operator_name"] = operator_name

	# if supervisor_name:
	# 	conditions.append("c.supervisor_name = %s")
	# 	params.append(supervisor_name)

	# if Casting_Treatment:
	# 	conditions.append("c.casting_treatment = %s")
	# 	params.append(Casting_Treatment)

	# if conditions:
	# 	sql_query += " AND " + " AND ".join(conditions)

	sql_query += """ GROUP BY heat_date,furnece """

	# frappe.throw(str(params))
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data