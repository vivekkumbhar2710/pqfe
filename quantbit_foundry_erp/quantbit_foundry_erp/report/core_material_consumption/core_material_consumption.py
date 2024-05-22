# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt
import frappe
def execute(filters=None):
	columns, data = get_col_data(), get_row_data(filters)
	return columns, data

def get_col_data():
	return [
		{
			'fieldname': 'Date', 'fieldtype': 'Date', 'label': 'Date'
		},
		{
			'fieldname': 'Shift', 'fieldtype': 'Data', 'label': 'Shift'
		},
		{
			'fieldname': 'Operator Id', 'fieldtype': 'Data', 'label': 'Operator Id'
		},
		{
			'fieldname': 'Operator Name', 'fieldtype': 'Data', 'label': 'Operator Name'
		},
		{
			'fieldname': 'PART NAME', 'fieldtype': 'Data', 'label': 'PART NAME'
		},
		{
			'fieldname': 'Core_Weight', 'fieldtype': 'Float', 'label': 'Core Weight'
		},
		{
			'fieldname': 'ACTUAL_QTY', 'fieldtype': 'Data', 'label': 'ACTUAL QTY'
		},
		{
			'fieldname': 'Actual Weight', 'fieldtype': 'Float', 'label': 'Actual Weight'
		},
		{
			'fieldname': 'REJECTION_QTY', 'fieldtype': 'Data', 'label': 'REJECTION QTY'
		},
		{
			'fieldname': 'REJECTION_Percentage', 'fieldtype': 'FLoat', 'label': 'REJECTION %'
		},
		{
			'fieldname': 'OK_QTY', 'fieldtype': 'Data', 'label': 'OK QTY'
		},
		{
			'fieldname': 'Ok Weight', 'fieldtype': 'Float', 'label': 'Ok Weight'
		}
	]

def get_row_data(filters):
	from_date, to_date, comp = filters.get("from_date"), filters.get("to_date"), filters.get("company")
	sql_query = """
			SELECT cwo.date AS 'Date', cwo.shift_time AS 'Shift', cwo.operator AS 'Operator Id', cwo.operator_name AS 'Operator Name', fid.item_code AS 'PART NAME',
			fid.okqty AS 'OK_QTY', fid.rejqty AS 'REJECTION_QTY', fid.updatedqty AS 'ACTUAL_QTY'
			FROM `tabComponent Work Order` cwo
			LEFT JOIN `tabFinished Item Details` fid ON cwo.name = fid.parent
			WHERE cwo.docstatus = '1' AND cwo.posting_date BETWEEN %(from_date)s AND %(to_date)s AND cwo.company = %(company)s
			"""
	data = frappe.db.sql(sql_query, {"from_date": from_date, "to_date": to_date, "company":comp}, as_dict=True)
	for entry in data:
		item_doc = frappe.get_doc("Item",{'name': entry['PART NAME']})
		if len(item_doc.custom_production_uom_definition)!=0:
			for i in item_doc.custom_production_uom_definition:
				core_weight = frappe.get_value("Production UOM Definition",{'name':i.name, 'uom': 'Kg'}, 'value_per_unit')
				if core_weight:
					entry['Core_Weight'] = core_weight
				else:
					entry['Core_Weight'] = 0.0
		else:
			entry['Core_Weight'] = 0.0
		entry['Actual Weight'] = entry['Core_Weight'] * entry['ACTUAL_QTY']
		entry['REJECTION_Percentage'] = round((entry['REJECTION_QTY']/entry['OK_QTY'])*100, 3)
		entry['Ok Weight'] = entry['Core_Weight'] * entry['OK_QTY']
	return data