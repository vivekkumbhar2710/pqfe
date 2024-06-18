# Copyright (c) 2024, Abhishek Chougule and contributors
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
			"fieldname": "name",
			"fieldtype": "Link",
			"label": "Receipt No",
			"options" : "Purchase Receipt"					
		},
		{
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"label": "Date"	
		},		
		{
			"fieldname": "supplier_delivery_note",
			"fieldtype": "Data",
			"label": "Supplier Delivery Note"
		},
		{
			"fieldname": "supplier",
			"fieldtype": "Data",
			"label": "Supplier Name"
		},
		{
			"fieldname": "purchase_order",
			"fieldtype": "Data",
			"label": "Purchase Order",
			"width":200
		},
		{
			"fieldname": "item_group",
			"fieldtype": "Data",
			"label": "Item Group",
			"width":200
		},
		{
			"fieldname": "item_code",
			"fieldtype": "Link",
			"label": "Item Code",
			"options": "Item",
		},
		{
			"fieldname": "item_name",
			"fieldtype": "Data",
			"label": "Item Name",
			"width":250
		},		
		{
			"fieldname": "received_qty",
			"fieldtype": "Float",
			"label": "Received Quantity"
		},
		{
			"fieldname": "uom",
			"fieldtype": "Data",
			"label": "UOM"
		},
		{
			"fieldname": "qty",
			"fieldtype": "Float",
			"label": "Accepted Quantity"
		},
		{
			"fieldname": "rejected_qty",
			"fieldtype": "Float",
			"label": "Rejected Quantity"
		},
		{
			"fieldname": "custom_weight",
			"fieldtype": "Float",
			"label": "Weight",
		},
		{
			"fieldname": "rate",
			"fieldtype": "Float",
			"label": "Rate (INR)",
			"width":100
		},
		{
			"fieldname": "amount",
			"fieldtype": "Float",
			"label": "Amount(INR)"
		},
		{
			"fieldname": "vehicle_no",
			"fieldtype": "Data",
			"label": "Vehicle No"
		},		
		{
			"fieldname": "company",
			"fieldtype": "Data",
			"label": "Company"
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
	item_group = filters.get("item_group")
	conditions = []
	params = [comp,from_date, to_date]

	sql_query = """
					SELECT 
						p.name 'name',
						p.posting_date 'posting_date',
						p.supplier_delivery_note 'supplier_delivery_note',
						p.supplier 'supplier',
						i.purchase_order 'purchase_order',
						i.item_code 'item_code', 
						i.item_name 'item_name',
						i.item_group 'item_group',
						i.received_qty 'received_qty', 
						i.uom 'uom', 
						i.qty 'qty', 
						i.rejected_qty 'rejected_qty',
						i.custom_weight 'custom_weight', 
						i.rate 'rate', 
						i.amount 'amount',
						p.vehicle_no 'vehicle_no',
						p.company 'company'
					FROM
						`tabPurchase Receipt` p
					LEFT JOIN
						`tabPurchase Receipt Item` i ON p.name = i.parent
					WHERE
						p.company = %s AND DATE(p.posting_date) BETWEEN %s AND %s AND p.docstatus = 1								
				"""
	

	if item_group:
		add_condition(conditions, params, "i.item_group in %s", item_group)

	if conditions:
		sql_query += " AND " + " AND ".join(conditions)

	sql_query += "GROUP BY p.name, p.posting_date, p.company, p.supplier_delivery_note,	i.purchase_order, i.item_code, i.item_name, i.received_qty, i.uom, i.qty, i.rejected_qty, i.total_weight, i.rate, i.amount,	p.vehicle_no"
	data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
	# frappe.throw(str(data))
	return data
