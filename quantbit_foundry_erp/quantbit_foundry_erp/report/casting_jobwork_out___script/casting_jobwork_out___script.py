import frappe
from datetime import datetime

def execute(filters=None):
    columns, data = [], []
    columns = get_col(filters.get("group_by"))
    data = get_data(filters)
    if not data:
        frappe.msgprint("No data")
    return columns, data

def get_col(group_by):
    columns = [
        {
            "fieldname": "Customer ID","fieldtype": "Data","label": "Customer ID"
        },
        {
            "fieldname": "Customer Name","fieldtype": "Data","label": "Customer Name"
        },
        {
            "fieldname": "Out Challan No","fieldtype": "Data","label": "Out Challan No"
        },
        {
            "fieldname": "In Challan No","fieldtype": "Data","label": "In Challan No"
        },
        {
            "fieldname": "opening_qty","fieldtype": "Float","label": "Opening Qty"
        },
        {
            "fieldname": "IN Qty","fieldtype": "Data","label": "In Qty"
        },
        {
            "fieldname": "total_qty","fieldtype": "Float","label": "Total Qty"
        },
        {
            "fieldname": "(OK) Return Quantity","fieldtype": "Float","label": "(OK) Return Quantity"
        },
        {
            "fieldname": "(OK) Return Quantity Weight","fieldtype": "Float","label": " (OK) Return Quantity Weight"
        },
        {
            "fieldname": "As It Is","fieldtype": "Float","label": "As It Is"
        },
        {
            
            "fieldname": "As It Is Weight","fieldtype": "Float","label": "As It Is Weight"
        },
        {
            "fieldname": "CR Rejection","fieldtype": "Float","label": "CR Rejection"
        },
        {
            "fieldname": "CR Rejection Weight","fieldtype": "Float","label": "CR Rejection Weight"
        },
        {
            "fieldname": "MR Rejection","fieldtype": "Float","label": "MR Rejection"
        },
        {
            "fieldname": "MR Rejection Weight","fieldtype": "Float","label": "MR Rejection Weight"
        },
        {
            "fieldname": "Other Rejection","fieldtype": "Float","label": "Other Rejection"
        },
        {
            "fieldname": "Other Rejection Weight","fieldtype": "Float","label": "Other Rejection Weight"
        },
        {
            "fieldname": "Total Quantity","fieldtype": "Float","label": "Total Quantity"
        },
        {
            "fieldname": "Total Quantity Weight","fieldtype": "Float","label": "Total Quantity Weight"
        },
        {
            "fieldname": "Balance","fieldtype": "Float","label": "Balance"
        }
    ]
    if group_by == "Group By Item":
        columns.insert(0, {"fieldname": "Item Code","fieldtype": "Data","label": "Item Code"})
        columns.insert(1,{"fieldname": "Item Name","fieldtype": "Data","label": "Item Name"})
    else:
        columns.insert(2, {"fieldname": "Item Code","fieldtype": "Data","label": "Item Code"})
        columns.insert(3,{"fieldname": "Item Name","fieldtype": "Data","label": "Item Name"})
    return columns

def get_data(filters):
    comp = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    group_by = filters.get("group_by")

    sql_query = """
        SELECT 
            j.name AS 'Out Challan No',
            j.customer AS 'Customer ID', 
            j.customer_name AS 'Customer Name', 
            ri.challan_reference AS 'In Challan No', 
            ri.item_name AS 'Item Name', 
            ri.item_code AS 'Item Code', 
            ri.as_it_is AS 'As It Is', 
            ri.returnable_quantity AS 'IN Qty',
            ((ri.as_it_is) * x.value_per_unit) AS 'As It Is Weight',
            ri.cr_rejection AS 'CR Rejection', 
            ((ri.cr_rejection) * x.value_per_unit) AS 'CR Rejection Weight',
            ri.mr_rejection AS 'MR Rejection', 
            ((ri.mr_rejection) * x.value_per_unit) AS 'MR Rejection Weight',
            ri.other_rejection AS 'Other Rejection', 
            ((ri.other_rejection) * x.value_per_unit) AS 'Other Rejection Weight',
            ri.return_quantity AS ' (OK) Return Quantity', 
            ((ri.return_quantity) * x.value_per_unit) AS '(OK) Return Quantity Weight',
            ri.total_quantity AS 'Total Quantity',
            ((ri.total_quantity) * x.value_per_unit) AS 'Total Quantity Weight',
            j.company AS 'Company'
        FROM
            `tabJob Work Receipt` j
        LEFT JOIN
            `tabReturn Job Work Receipt Item` ri ON j.name = ri.parent
        LEFT JOIN
            (SELECT 
                rec.parent AS 'parent', 
                i.name, 
                pu.value_per_unit 
            FROM
                `tabItem` i
            LEFT JOIN 
                `tabProduction UOM Definition` pu ON i.name = pu.parent
            LEFT JOIN
                `tabReturn Job Work Receipt Item` rec ON i.name = rec.item_code) x 
        ON j.name = x.parent AND ri.item_code = x.name
        WHERE
            j.docstatus = '1'
            AND j.is_return = '1'
            AND j.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND j.company = %(company)s
        GROUP BY
            j.customer, 
            j.customer_name, 
            ri.challan_reference, 
            ri.item_name
    """
    data = frappe.db.sql(sql_query, {"from_date": from_date, "to_date": to_date, "company": comp}, as_dict=True)
    
    for entry in data:
        warehouse = frappe.get_value("Job Work Receipt",{'name': entry['In Challan No']},'set_warehouse')
        opening_qty = get_all_opening_qty(entry['Item Code'], warehouse, filters)
        entry['opening_qty'] = opening_qty

        posting_date = frappe.get_value("Job Work Receipt",{'name': entry['In Challan No']},'posting_date')
        from_d, to_d, post_d = datetime.strptime(from_date, "%Y-%m-%d"), datetime.strptime(to_date, "%Y-%m-%d"), datetime.strptime(str(posting_date), "%Y-%m-%d")
        if from_d <= post_d <= to_d:
            entry['total_qty'] = entry['opening_qty'] + entry['IN Qty']
        else:
            entry['total_qty'] = entry['opening_qty']
            entry['IN Qty'] = 0
        entry['Balance'] = entry['total_qty'] - entry['Total Quantity']

    if group_by == "Group By Item":
        sorted_data = sorted(data, key=lambda x: x['Item Code'])
        subtotal = {
            'Item Code': None,
            'Item Name': None,
            'Customer ID': None,
            'Customer Name': None,
            'Out Challan No': None,
            'In Challan No': None,
            'opening_qty': 0.0,
            'IN Qty': 0.0,
            'total_qty': 0.0,
            '(OK) Return Quantity': 0.0,
            '(OK) Return Quantity Weight': 0.0,
            'As It Is': 0.0,
            'As It Is Weight': 0.0,
            'CR Rejection': 0.0,
            'CR Rejection Weight': 0.0,
            'MR Rejection': 0.0,
            'MR Rejection Weight': 0.0,
            'Other Rejection': 0.0,
            'Other Rejection Weight': 0.0,
            'Total Quantity': 0.0,
            'Total Quantity Weight': 0.0,
            'Balance': 0.0
        }
        result = []
        current_item_code = None
        for entry in sorted_data:
            if entry['Item Code'] != current_item_code:
                if current_item_code is not None:
                    subtotal['Item Code'] = 'Sub Total'
                    result.append(subtotal.copy())
                    subtotal = subtotal.fromkeys(subtotal, 0.0)
                    # subtotal['Item Code'] = 'Subtotal'
                current_item_code = entry['Item Code']
                subtotal['Item Code'] = 'Sub Total'
            for key in subtotal.keys():
                if key not in ['Item Code', 'Item Name', 'Customer ID', 'Customer Name','Out Challan No', 'In Challan No']:
                    subtotal[key] += entry[key]
                else:
                    if key != 'Item Code':
                        subtotal[key] = None
            result.append(entry)
        result.append(subtotal)

    if group_by == "Group By Customer":
        sorted_data = sorted(data, key=lambda x: x['Customer ID'])
        subtotal = {
            'Item Code': None,
            'Item Name': None,
            'Customer ID': None,
            'Customer Name': None,
            'Out Challan No': None,
            'In Challan No': None,
            'opening_qty': 0.0,
            'IN Qty': 0.0,
            'total_qty': 0.0,
            '(OK) Return Quantity': 0.0,
            '(OK) Return Quantity Weight': 0.0,
            'As It Is': 0.0,
            'As It Is Weight': 0.0,
            'CR Rejection': 0.0,
            'CR Rejection Weight': 0.0,
            'MR Rejection': 0.0,
            'MR Rejection Weight': 0.0,
            'Other Rejection': 0.0,
            'Other Rejection Weight': 0.0,
            'Total Quantity': 0.0,
            'Total Quantity Weight': 0.0,
            'Balance': 0.0
        }
        result = []
        current_cust_id = None
        for entry in sorted_data:
            if entry['Customer ID'] != current_cust_id:
                if current_cust_id is not None:
                    subtotal['Customer ID'] = 'Sub Total'
                    result.append(subtotal.copy())
                    subtotal = subtotal.fromkeys(subtotal, 0.0)
                    # subtotal['Item Code'] = 'Subtotal'
                current_cust_id = entry['Customer ID']
                subtotal['Customer ID'] = 'Sub Total'
            for key in subtotal.keys():
                if key not in ['Item Code', 'Item Name', 'Customer ID', 'Customer Name','Out Challan No', 'In Challan No']:
                    subtotal[key] += entry[key]
                else:
                    if key != 'Customer ID':
                        subtotal[key] = None
            result.append(entry)
        result.append(subtotal)
    
    return result


def get_all_opening_qty(item_code, warehouse,filters):
    from_date, to_date = filters.get('from_date'), filters.get('to_date')
    company_name = filters.get('company')

    opn_sum = 0
    opening_balance = frappe.db.sql("""
        SELECT qty_after_transaction 
        FROM `tabStock Ledger Entry` 
        WHERE posting_date < '{0}' 
            AND warehouse = '{1}' 
            AND item_code = '{2}' 
            AND company = '{3}' 
            AND is_cancelled='{4}'
        ORDER BY creation DESC 
        LIMIT 1
        """.format(to_date, warehouse, item_code, company_name, False), as_dict=True)
    if opening_balance:
        opn_sum = opening_balance[0].qty_after_transaction
    return opn_sum
