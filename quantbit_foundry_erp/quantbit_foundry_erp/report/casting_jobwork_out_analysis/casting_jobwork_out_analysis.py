# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
    columns, data = [], []
    columns = get_col(filters)
    data = get_data(filters)
    return columns, data

def get_col(filters):
    columns = [{
            "fieldname": "Customer_ID","fieldtype": "Data","label": "Customer ID"},{
            "fieldname": "Customer_Name","fieldtype": "Data","label": "Customer Name"},{
            # "fieldname": "Challan_No","fieldtype": "Data","label": "Out Challan No"},{
            "fieldname": "Accepted_Quantity","fieldtype": "Float","label": "Accepted Quantity"},{
            "fieldname": "Return_Quantity","fieldtype": "Float","label": "Return Quantity"},{
            "fieldname": "opening_qty","fieldtype": "Float","label": "Opening Qty"},{
            "fieldname": "IN_Qty","fieldtype": "Data","label": "In Qty"},{
            "fieldname": "total_qty","fieldtype": "Float","label": "Total Qty"},{
            "fieldname": "OK_Return_Quantity","fieldtype": "Float","label": "(OK) Return Quantity"},{
            "fieldname": "As_It_Is","fieldtype": "Float","label": "As It Is"},{
            "fieldname": "CR_Rejection","fieldtype": "Float","label": "CR Rejection"},{
            "fieldname": "MR_Rejection","fieldtype": "Float","label": "MR Rejection"},{
            "fieldname": "Other_Rejection","fieldtype": "Float","label": "Other Rejection"},{
            "fieldname": "Total_Quantity","fieldtype": "Float","label": "Total Quantity"},{
            "fieldname": "Balance","fieldtype": "Float","label": "Balance"}]
    
    if filters.get("group_by") == "Group By Item":
        columns.insert(0, {"fieldname": "Item_Code","fieldtype": "Data","label": "Item Code"})
        columns.insert(1,{"fieldname": "Item_Name","fieldtype": "Data","label": "Item Name"})
    else:
        columns.insert(2, {"fieldname": "Item_Code","fieldtype": "Data","label": "Item Code"})
        columns.insert(3,{"fieldname": "Item_Name","fieldtype": "Data","label": "Item Name"})

    if filters.get("include_weight"):
        columns.insert(11,{"fieldname": "OK_Return_Quantity_Weight","fieldtype": "Float","label": " (OK) Return Quantity Weight"})
        columns.insert(13,{"fieldname": "As_It_Is_Weight","fieldtype": "Float","label": "As It Is Weight"})
        columns.insert(15,{"fieldname": "CR_Rejection_Weight","fieldtype": "Float","label": "CR Rejection Weight"})
        columns.insert(17,{"fieldname": "MR_Rejection_Weight","fieldtype": "Float","label": "MR Rejection Weight"})
        columns.insert(19,{"fieldname": "Other_Rejection_Weight","fieldtype": "Float","label": "Other Rejection Weight"})
        columns.insert(21,{"fieldname": "Total_Quantity_Weight","fieldtype": "Float","label": "Total Quantity Weight"})
    return columns

def get_data(filters):
    comp = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    group_by = filters.get("group_by")

    sql_query = """
        SELECT 
            Date,
            Challan_No,
            Company, 
            Customer_ID, 
            Customer_Name, 
            Item_Name, 
            Item_Code, 
            Warehouse,
            SUM(Accepted_Quantity) AS 'Accepted_Quantity', 
            SUM(Return_Quantity) AS 'Return_Quantity',
            SUM(IN_Qty) AS 'IN_Qty',
            SUM(As_It_Is) AS 'As_It_Is', 
            SUM(As_It_Is_Weight) AS 'As_It_Is_Weight',
            SUM(CR_Rejection) AS 'CR_Rejection', 
            SUM(CR_Rejection_Weight) AS 'CR_Rejection_Weight',
            SUM(MR_Rejection) AS 'MR_Rejection',
            SUM(MR_Rejection_Weight) AS 'MR_Rejection_Weight', 
            SUM(Other_Rejection) AS 'Other_Rejection',
            SUM(Other_Rejection_Weight) AS 'Other_Rejection_Weight',
            SUM(OK_Return_Quantity) AS 'OK_Return_Quantity',
            SUM(OK_Return_Quantity_Weight) AS 'OK_Return_Quantity_Weight',
            SUM(Total_Quantity) AS 'Total_Quantity',
            SUM(Total_Quantity_Weight) AS 'Total_Quantity_Weight' 
        FROM (
            SELECT j.posting_date AS Date, j.name AS 'Challan_No', j.customer AS 'Customer_ID',  j.customer_name AS 'Customer_Name',  ri.item_name AS 'Item_Name',  ri.item_code AS 'Item_Code',  j.set_warehouse AS Warehouse, ri.qty AS 'Accepted_Quantity', ri.return_quantity AS 'Return_Quantity',
                0 AS 'As_It_Is', 
                0 AS 'IN_Qty',
                0 AS 'As_It_Is_Weight',
                0 AS 'CR_Rejection', 
                0 AS 'CR_Rejection_Weight',
                0 AS 'MR_Rejection', 
                0 AS 'MR_Rejection_Weight',
                0 AS 'Other_Rejection', 
                0 AS 'Other_Rejection_Weight',
                0 AS 'OK_Return_Quantity', 
                0 AS 'OK_Return_Quantity_Weight',
                0 AS 'Total_Quantity',
                0 AS 'Total_Quantity_Weight',
                j.company AS 'Company'
            FROM
                `tabJob Work Receipt` j
            LEFT JOIN
                `tabJob Work Receipt Item` ri ON j.name = ri.parent
            LEFT JOIN (
                SELECT 
                    rec.parent AS 'parent', 
                    i.name, 
                    pu.value_per_unit 
                FROM
                    `tabItem` i
                LEFT JOIN 
                    `tabProduction UOM Definition` pu ON i.name = pu.parent
                LEFT JOIN
                    `tabJob Work Receipt Item` rec ON i.name = rec.item_code
            ) x ON j.name = x.parent AND ri.item_code = x.name
            WHERE 
                j.docstatus = '1' AND 
                j.posting_date BETWEEN %(from_date)s AND %(to_date)s AND 
                j.company = %(company)s

            UNION ALL

            SELECT j.posting_date AS Date, j.name AS 'Challan_No', j.customer AS 'Customer_ID',  j.customer_name AS 'Customer_Name',  ri.item_name AS 'Item_Name',  ri.item_code AS 'Item_Code', NULL AS Warehouse,
                0 AS 'Accepted_Quantity', 0 AS 'Return_Quantity',
                ri.as_it_is AS 'As_It_Is', 
                ri.returnable_quantity AS 'IN_Qty',
                ((ri.as_it_is) * x.value_per_unit) AS 'As_It_Is_Weight',
                ri.cr_rejection AS 'CR_Rejection', 
                ((ri.cr_rejection) * x.value_per_unit) AS 'CR_Rejection_Weight',
                ri.mr_rejection AS 'MR_Rejection', 
                ((ri.mr_rejection) * x.value_per_unit) AS 'MR_Rejection_Weight',
                ri.other_rejection AS 'Other_Rejection', 
                ((ri.other_rejection) * x.value_per_unit) AS 'Other_Rejection_Weight',
                ri.return_quantity AS 'OK_Return_Quantity', 
                ((ri.return_quantity) * x.value_per_unit) AS 'OK_Return_Quantity_Weight',
                ri.total_quantity AS 'Total_Quantity',
                ((ri.total_quantity) * x.value_per_unit) AS 'Total_Quantity_Weight',
                j.company AS 'Company'
            FROM
                `tabJob Work Receipt` j
            LEFT JOIN
                `tabReturn Job Work Receipt Item` ri ON j.name = ri.parent
            LEFT JOIN (
                SELECT 
                    rec.parent AS 'parent', 
                    i.name, 
                    pu.value_per_unit 
                FROM
                    `tabItem` i
                LEFT JOIN 
                    `tabProduction UOM Definition` pu ON i.name = pu.parent
                LEFT JOIN
                    `tabReturn Job Work Receipt Item` rec ON i.name = rec.item_code
            ) x ON j.name = x.parent AND ri.item_code = x.name
            WHERE
                j.docstatus = '1' AND 
                j.is_return = '1' AND 
                j.posting_date BETWEEN %(from_date)s AND %(to_date)s AND 
                j.company = %(company)s
        ) c
        GROUP BY
            Customer_ID,
            Item_Code
    """

    data = frappe.db.sql(sql_query, {"from_date": from_date, "to_date": to_date, "company": comp}, as_dict=True)
    # filtered_data = []
    # for dt in data:
    #     if dt.get('Item_Code') != 'None':
    #         filtered_data.append(dt)
    # data = filtered_data
    data[:] = [dt for dt in data if dt.get('Item_Code') is not None]
    # frappe.throw(str(data))
    for entry in data:
        opening_qty = get_all_opening_qty(entry['Item_Code'], entry['Warehouse'], filters)
        entry['opening_qty'] = opening_qty

        # posting_date = frappe.get_value("Job Work Receipt",{'name': entry['In_Challan_No']},'posting_date')
        from_d, to_d, post_d = datetime.strptime(from_date, "%Y-%m-%d"), datetime.strptime(to_date, "%Y-%m-%d"), datetime.strptime(str(entry['Date']), "%Y-%m-%d")
        if from_d <= post_d <= to_d:
            entry['total_qty'] = entry['opening_qty'] + entry['IN_Qty']
        else:
            entry['total_qty'] = entry['opening_qty']
            entry['IN_Qty'] = 0
        entry['Balance'] = entry['total_qty'] - entry['Total_Quantity']

    if group_by == "Group By Item":
        sorted_data = sorted(data, key=lambda x: (x["Item_Code"] is None, x["Item_Code"]))
        subtotal = {
            'Date': None,
            'Warehouse':None,
            'Item_Code': None,
            'Item_Name': None,
            'Customer_ID': None,
            'Customer_Name': None,
            'Challan_No': None,
            'Accepted_Quantity':0.0,
            'Return_Quantity':0.0,
            'opening_qty': 0.0,
            'IN_Qty': 0.0,
            'total_qty': 0.0,
            'OK_Return_Quantity': 0.0,
            'OK_Return_Quantity_Weight': 0.0,
            'As_It_Is': 0.0,
            'As_It_Is_Weight': 0.0,
            'CR_Rejection': 0.0,
            'CR_Rejection_Weight': 0.0,
            'MR_Rejection': 0.0,
            'MR_Rejection_Weight': 0.0,
            'Other_Rejection': 0.0,
            'Other_Rejection_Weight': 0.0,
            'Total_Quantity': 0.0,
            'Total_Quantity_Weight': 0.0,
            'Balance': 0.0
        }
        result = []
        current_item_code = None
        for entry in sorted_data:
            if entry['Item_Code'] != current_item_code:
                if current_item_code is not None:
                    subtotal['Item_Code'] = 'Sub Total'
                    result.append(subtotal.copy())
                    subtotal = subtotal.fromkeys(subtotal, 0.0)
                    # subtotal['Item_Code'] = 'Subtotal'
                current_item_code = entry['Item_Code']
                subtotal['Item_Code'] = 'Sub Total'
            for key in subtotal.keys():
                if key not in ['Date','Warehouse','Item_Code', 'Item_Name', 'Customer_ID', 'Customer_Name','Challan_No']:
                    if entry[key]:
                        subtotal[key] += entry[key]
                    else:
                        subtotal[key] += 0.0
                else:
                    if key != 'Item_Code':
                        subtotal[key] = None
            result.append(entry)
        result.append(subtotal)

    if group_by == "Group By Customer":
        sorted_data = sorted(data, key=lambda x: (x["Customer_ID"] is None, x["Customer_ID"]))
        subtotal = {
            'Date': None,
            'Warehouse':None,
            'Item_Code': None,
            'Item_Name': None,
            'Customer_ID': None,
            'Customer_Name': None,
            'Challan_No': None,
            'Accepted_Quantity':0.0,
            'Return_Quantity':0.0,
            'opening_qty': 0.0,
            'IN_Qty': 0.0,
            'total_qty': 0.0,
            'OK_Return_Quantity': 0.0,
            'OK_Return_Quantity_Weight': 0.0,
            'As_It_Is': 0.0,
            'As_It_Is_Weight': 0.0,
            'CR_Rejection': 0.0,
            'CR_Rejection_Weight': 0.0,
            'MR_Rejection': 0.0,
            'MR_Rejection_Weight': 0.0,
            'Other_Rejection': 0.0,
            'Other_Rejection_Weight': 0.0,
            'Total_Quantity': 0.0,
            'Total_Quantity_Weight': 0.0,
            'Balance': 0.0
        }
        result = []
        current_cust_id = None
        for entry in sorted_data:
            if entry['Customer_ID'] != current_cust_id:
                if current_cust_id is not None:
                    subtotal['Customer_ID'] = 'Sub Total'
                    result.append(subtotal.copy())
                    subtotal = subtotal.fromkeys(subtotal, 0.0)
                    # subtotal['Item_Code'] = 'Subtotal'
                current_cust_id = entry['Customer_ID']
                subtotal['Customer_ID'] = 'Sub Total'
            for key in subtotal.keys():
                if key not in ['Date','Warehouse','Item_Code', 'Item_Name', 'Customer_ID', 'Customer_Name','Challan_No']:
                    if entry[key]:
                        subtotal[key] += entry[key]
                    else:
                        subtotal[key] += 0.0
                else:
                    if key != 'Customer_ID':
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




