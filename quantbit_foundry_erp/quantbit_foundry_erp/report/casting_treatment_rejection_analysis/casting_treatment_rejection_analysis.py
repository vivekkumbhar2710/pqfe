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
			"fieldtype" : "Link",
			"options":"Casting Treatment",
			"label" : "Document Id"
		},
		{
			"fieldname" : "casting_treatment",
			"fieldtype" : "Data",
			"label" : "Casting Treatment",
			"width":180
		},
		{
			"fieldname" : "supervisor_name",
			"fieldtype" : "Data",
			"label" : "Supervisor Name",
			"width":200
		},
		{
			"fieldname" : "contractor_id",
			"fieldtype" : "Link",
			"options" : "Supplier",
			"label" : "Contractor ID",
			"precision": 3,
			"width":150
		},
		{
			"fieldname" : "contractor_name",
			"fieldtype" : "Data",
			"label" : "Contractor Name",
			"width":200		
		},
		{
			"fieldname" : "item_code",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Finished Item Code",
			"width":280
		},
		{
			"fieldname" : "item_name",
			"fieldtype" : "Data",
			"label" : "Finished Item Name",
			"width":280
		},
		{
			"fieldname" : "rejection_reason",
			"fieldtype" : "Data",
			"label" : "Rejection Reason"
		},
		{
			"fieldname" : "rejection_type",
			"fieldtype" : "Data",
			"label" : "Rejection Type"
		},
		{
			"fieldname" : "qty",
			"fieldtype" : "Float",
			"label" : "Quantity",
			"precision": 3			
		},		
		
		{
			"fieldname" : "total_weight",
			"fieldtype" : "Float",
			"label" : "Total Weight",
			"precision": 3
		},
		
		{
			"fieldname" : "is_scrap",
			"fieldtype" : "Data",
			"label" : "Is Scrap"
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
	item = filters.get("item_code")
	sup_name = filters.get("supervisor")
	contractor_name = filters.get("contractor")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
						c.name 'name',
						c.company 'company',
						c.casting_treatment 'casting_treatment',
						c.supervisor_name 'supervisor_name',
						r.item_code 'item_code',
						r.item_name 'item_name',
						SUM(r.qty) 'qty',
						r.contractor_id 'contractor_id',
						r.contractor_name 'contractor_name',
						r.grade 'grade',
						SUM(r.total_weight) 'total_weight',
						r.rejection_reason 'rejection_reason',
						r.rejection_type 'rejection_type',
						(CASE WHEN r.is_scrap = 1 THEN "Yes" ELSE "No" END) AS 'is_scrap'									
					FROM
						`tabCasting Treatment` c
					LEFT JOIN
						`tabCasting Treatment Rejected Items Reasons` r ON c.name = r.parent
					WHERE c.company = %s 
						AND DATE(c.treatment_date) BETWEEN %s AND %s 
						AND c.docstatus = 1 
						AND r.rejection_reason IS NOT NULL					
				"""
    
	if sup_name:
		add_condition(conditions, params, "c.supervisor in %s", sup_name)
	
	if item:
		add_condition(conditions, params, "r.item_code in %s", item)
	
	if contractor_name:
		add_condition(conditions, params, "r.contractor_id in %s", contractor_name)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY c.name, c.company, c.casting_treatment, c.supervisor_name, r.item_code, r.item_name, r.contractor_id, r.contractor_name,	r.rejection_reason, r.rejection_type, r.grade"

	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	return data
