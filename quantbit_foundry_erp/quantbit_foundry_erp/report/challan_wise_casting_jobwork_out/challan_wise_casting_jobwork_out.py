import frappe
from datetime import datetime

def execute(filters=None):
    columns, data = [], []
    columns = get_col(filters)
    data = get_data(filters)
    return columns, data

def get_col(filters):
    columns = [
        {"fieldname": "Out Challan No", "fieldtype": "Data", "label": "Out Challan No"},
        {"fieldname": "In Challan No", "fieldtype": "Data", "label": "In Challan No"},
        {"fieldname": "Customer Name", "fieldtype": "Data", "label": "Customer Name"},
        {"fieldname": "Item Code", "fieldtype": "Data", "label": "Item Code"},
        {"fieldname": "Item Name", "fieldtype": "Data", "label": "Item Name"},
        {"fieldname": "opening_qty", "fieldtype": "Float", "label": "Opening Qty"},
        {"fieldname": "IN Qty", "fieldtype": "Data", "label": "In Qty"},
        {"fieldname": "total_qty", "fieldtype": "Float", "label": "Total Qty"},
        {"fieldname": "(OK) Return Quantity", "fieldtype": "Float", "label": "(OK) Return Quantity"},
        {"fieldname": "As It Is", "fieldtype": "Float", "label": "As It Is"},
        {"fieldname": "CR Rejection", "fieldtype": "Float", "label": "CR Rejection"},
        {"fieldname": "MR Rejection", "fieldtype": "Float", "label": "MR Rejection"},
        {"fieldname": "Other Rejection", "fieldtype": "Float", "label": "Other Rejection"},
        {"fieldname": "Total Quantity", "fieldtype": "Float", "label": "Total Quantity"},
        {"fieldname": "Balance", "fieldtype": "Float", "label": "Balance"}
    ]

    if filters.get("include_weight"):
        columns.insert(9, {"fieldname": "(OK) Return Quantity Weight", "fieldtype": "Float", "label": "(OK) Return Quantity Weight"})
        columns.insert(11, {"fieldname": "As It Is Weight", "fieldtype": "Float", "label": "As It Is Weight"})
        columns.insert(13, {"fieldname": "CR Rejection Weight", "fieldtype": "Float", "label": "CR Rejection Weight"})
        columns.insert(15, {"fieldname": "MR Rejection Weight", "fieldtype": "Float", "label": "MR Rejection Weight"})
        columns.insert(17, {"fieldname": "Other Rejection Weight", "fieldtype": "Float", "label": "Other Rejection Weight"})
        columns.insert(19, {"fieldname": "Total Quantity Weight", "fieldtype": "Float", "label": "Total Quantity Weight"})

    return columns

def get_data(filters):
    comp = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    out = filters.get("Out Challan No")

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
            ri.return_quantity AS '(OK) Return Quantity', 
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
            AND j.posting_date BETWEEN %s AND %s
            AND j.company = %s
    """

    conditions = []
    params = [from_date, to_date, comp]
    if out:
        conditions.append("j.name = %s")
        params.append(out)

    if conditions:
        sql_query += " AND " + " AND ".join(conditions)

    sql_query += " GROUP BY j.customer, j.customer_name, ri.challan_reference, ri.item_name"

    data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
    sorted_data = sorted(data, key=lambda x: x['Out Challan No'])

    for entry in sorted_data:
        warehouse = frappe.get_value("Job Work Receipt", {'name': entry['In Challan No']}, 'set_warehouse')
        opening_qty = get_all_opening_qty(entry['Item Code'], warehouse, filters)
        entry['opening_qty'] = opening_qty

        posting_date = frappe.get_value("Job Work Receipt", {'name': entry['In Challan No']}, 'posting_date')
        from_d = datetime.strptime(from_date, "%Y-%m-%d")
        to_d = datetime.strptime(to_date, "%Y-%m-%d")
        post_d = datetime.strptime(str(posting_date), "%Y-%m-%d")

        if from_d <= post_d <= to_d:
            entry['total_qty'] = entry['opening_qty'] + entry['IN Qty']
        else:
            entry['total_qty'] = entry['opening_qty']
            entry['IN Qty'] = 0

        entry['Balance'] = entry['total_qty'] - entry['Total Quantity']

    return sorted_data

def get_all_opening_qty(item_code, warehouse, filters):
    to_date = filters.get('to_date')
    company_name = filters.get('company')

    opn_sum = 0
    opening_balance = frappe.db.sql("""
        SELECT qty_after_transaction 
        FROM `tabStock Ledger Entry` 
        WHERE posting_date < %s
            AND warehouse = %s
            AND item_code = %s
            AND company = %s
            AND is_cancelled = %s
        ORDER BY creation DESC 
        LIMIT 1
    """, (to_date, warehouse, item_code, company_name, False), as_dict=True)
    
    if opening_balance:
        opn_sum = opening_balance[0].qty_after_transaction

    return opn_sum
