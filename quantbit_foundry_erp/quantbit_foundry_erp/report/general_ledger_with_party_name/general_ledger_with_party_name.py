# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe

from erpnext.accounts.report.general_ledger.general_ledger import execute as gl_entry

def get_party_name(party_type, party):
    if party_type and party:
        if party_type == 'Customer':
            return frappe.db.get_value('Customer', party, 'customer_name')
        elif party_type == 'Supplier':
            return frappe.db.get_value('Supplier', party, 'supplier_name')
        elif party_type == 'Employee':
            return frappe.db.get_value('Employee', party, 'employee_name')
        # Add other party types here if needed
    return ""

def execute(filters=None):
    columns, data = gl_entry(filters)
    party_type_index = next((index for (index, d) in enumerate(columns) if d['fieldname'] == 'party_type'), None)
    party_index = next((index for (index, d) in enumerate(columns) if d['fieldname'] == 'party'), None)
    
    party_name_column = {'label': 'Party Name', 'fieldname': 'party_name', 'fieldtype': 'Data', 'width': 200}
    columns.insert(party_index + 1, party_name_column)
    
    # Update data to include Party Name
    for row in data:
        if isinstance(row, dict):  # Ensure row is a dictionary
            party_type = row.get('party_type')
            party = row.get('party')
            row['party_name'] = get_party_name(party_type, party)
    
    # Left align the header of the 'Party Name' column
    party_name_column['align'] = 'left'
    
    return columns, data






