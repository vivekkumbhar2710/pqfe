# Copyright (c) 2024, quantdairy and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}
    columns, data = [], []

    company = filters.get('company')
    charge_item = frappe.db.sql(''' 
        SELECT c.item_code, c.item_name, c.name 
        FROM `tabGrade Master` p
        LEFT JOIN `tabGrade Items Details` c ON p.name = c.parent
        WHERE p.company = %s
        GROUP BY c.item_code 
    ''', (company), as_dict=True)

    columns = get_columns(charge_item)
    data = get_data(filters, charge_item)

    return columns, data

def get_columns(charge_item):
    return_col = [
        {
            "fieldname": "Pouring_Id",
            "fieldtype": "Link",
            "label": "Pouring Id",
            "options": "Pouring",
        },
        {
            "fieldname": "Heat_Date",
            "fieldtype": "Date",
            "label": "Heat Date",
        },
        {
            "fieldname": "Heat_No",
            "fieldtype": "Link",
            "label": "Heat No",
            "options": "Pouring",
        },
        {
            "fieldname": "Company",
            "fieldtype": "Link",
            "label": "Company",
            "options": "Company",
        },
    ]

    for d in charge_item:
        item_data = {
            "fieldname": d.item_code,
            "fieldtype": "Float",
            "label": d.item_name,
        }
        return_col.append(item_data)

    # Adding the total column
    return_col.append({
        "fieldname": "Total",
        "fieldtype": "Float",
        "label": "Total",
    })

    return return_col

def get_data(filters, charge_item):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    pouring_id = filters.get('Pouring_Id')
    heat_no = filters.get('Heat_No')
    company = filters.get('company')
    conditions = []
    params = [company, from_date, to_date]

    query_1 = """
        SELECT 
            pouring_id AS "Pouring_Id", 
            heat_date AS "Heat_Date",
            heat_no AS "Heat_No", 
            company AS "Company"
    """

    query_2 = """
        FROM (
            SELECT
                p.name AS pouring_id, 
                p.heat_date AS heat_date,
                p.heat_no AS heat_no,
                p.company AS company,
                c.item_code, 
                c.item_name, 
                c.quantity
    """

    query_3 = """
        FROM 
            `tabPouring` p 
        LEFT JOIN 
            `tabChange Mix Details` c ON p.name = c.parent 
        WHERE 
            p.docstatus = 1 AND p.company = %s 
            AND p.heat_date BETWEEN %s AND %s
    """

    for d in charge_item:
        string = str(d.item_code)
        string = string.replace("-", "")
        string = string.replace(".", "")
        item_name = string.replace(" ", "")

        a = ', SUM(' + item_name + ') AS "' + d.item_code + '"'
        query_1 += a

        b = ', CASE WHEN c.item_code = "' + d.item_code + '" THEN c.quantity ELSE 0 END AS ' + item_name
        query_2 += b

    # Adding the total calculation
    total_query = " + ".join(['COALESCE(SUM(' + str(d.item_code).replace("-", "").replace(".", "").replace(" ", "") + '), 0)' for d in charge_item])
    query_1 += f", ({total_query}) AS `Total`"

    sql_query = query_1 + query_2 + query_3

    if pouring_id:
        conditions.append("p.name in %s")
        params.append(pouring_id)
        
    if heat_no:
        conditions.append("p.heat_no = %s")
        params.append(heat_no)

    if conditions:
        sql_query += " AND " + " AND ".join(conditions)

    sql_query += " ) x GROUP BY pouring_id, heat_date, heat_no, company"

    data = frappe.db.sql(sql_query, tuple(params), as_dict=True)
    return data


	# {
	# 	"fieldname": "MS_SCRAP",
	# 	"fieldtype": "Link",
	# 	"label": "MS_SCRAP",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "CI_BORING",
	# 	"fieldtype": "Link",
	# 	"label": "CI_BORING",
	# 	"options": "Item",
	# },		
	# {
	# 	"fieldname": "PIG_IRON",
	# 	"fieldtype": "Link",
	# 	"label": "PIG_IRON",
	# 	"options": "Item",
	# },
	# 		{
	# 	"fieldname": "RR_CI_GRADE",
	# 	"fieldtype": "Link",
	# 	"label": "RR_CI_GRADE",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "CALCINED_PETROLIUM_COKE",
	# 	"fieldtype": "Link",
	# 	"label": "CALCINED_PETROLIUM_COKE",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "FERRO_SILICON_LUMPS",
	# 	"fieldtype": "Link",
	# 	"label": "FERRO_SILICON_LUMPS",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "FERRO_MANGANESE_LUMPS",
	# 	"fieldtype": "Link",
	# 	"label": "FERRO_MANGANESE_LUMPS",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "COPPER_SCRAP",
	# 	"fieldtype": "Link",
	# 	"label": "COPPER_SCRAP",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "INNOCULANT_BERINOC",
	# 	"fieldtype": "Link",
	# 	"label": "INNOCULANT_BERINOC",
	# 	"options": "Item",
	# },				
	# {
	# 	"fieldname": "SLAG_REMOVING_POWDER",
	# 	"fieldtype": "Link",
	# 	"label": "SLAG_REMOVING_POWDER",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "HEAL_METAL",
	# 	"fieldtype": "Link",
	# 	"label": "HEAL_METAL",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "MS_BAR",
	# 	"fieldtype": "Link",
	# 	"label": "MS_BAR",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "CRC_SCRAP",
	# 	"fieldtype": "Link",
	# 	"label": "CRC_SCRAP",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "SLAG_HOLDING_COMPOUND",
	# 	"fieldtype": "Link",
	# 	"label": "SLAG_HOLDING_COMPOUND",
	# },
	# {
	# 	"fieldname": "PIG_IRON_SG",
	# 	"fieldtype": "Link",
	# 	"label": "PIG_IRON_SG",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "RR_SG_GRADE",
	# 	"fieldtype": "Link",
	# 	"label": "RR_SG_GRADE",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "GRAPHITE_CARBON_GRANUAL",
	# 	"fieldtype": "Link",
	# 	"label": "GRAPHITE_CARBON_GRANUAL",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "RESEED_1_3MM",
	# 	"fieldtype": "Link",
	# 	"label": "RESEED_1_3MM",
	# 	"options": "Item",
	# },
	# {
	# 	"fieldname": "FERRO_SILICON_MAGNESIUM_ELMAG_6225",
	# 	"fieldtype": "Link",
	# 	"label": "FERRO_SILICON_MAGNESIUM_ELMAG_6225",
	# 	"options": "Item",
	# },		
	# {
	# 	"fieldname": "FERRO_SILICON_MAGNESIUM_ELMAG_5800",
	# 	"fieldtype": "Link",
	# 	"label": "FERRO_SILICON_MAGNESIUM_ELMAG_5800",
	# 	"options": "Item",
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



	# frappe.throw(str(sql_query))
# sql_query = """
# 			SUM(MSSCRAP) AS 'MS_SCRAP',
# 			SUM(CIBORING) AS "CI_BORING",
# 			SUM(PIGIRON) AS 'PIG_IRON',
# 			SUM(RRCIGRADE) AS 'RR_CI_GRADE',
# 			SUM(CALCINEDPETROLIUMCOKE) AS 'CALCINED_PETROLIUM_COKE',
# 			SUM(FERROSILICONLUMPS) AS 'FERRO_SILICON_LUMPS',
# 			SUM(FERROMANGANESELUMPS) AS 'FERRO_MANGANESE_LUMPS',
# 			SUM(FERROCHROMIUMLUMPS) AS 'FERRO_CHROMIUM_LUMPS',
# 			sum(COPPERSCRAP) as 'COPPER_SCRAP',
# 			SUM(INNOCULANTBERINOCCI) AS 'INNOCULANT_BERINOC - CI',
# 			SUM(SLAGREMOVINGPOWDER) AS 'SLAG_REMOVING_POWDER',
# 			SUM(HEALMETAL) AS 'HEAL_METAL',
# 			SUM(MSBAR) AS 'MS_BAR',
# 			SUM(CRCSCRAP) AS 'CRC_SCRAP',
# 			SUM(SLAGHOLDINGCOMPOUND) AS 'SLAG_HOLDING_COMPOUND',
# 			sum(PIGIRONG) as 'PIG_IRON_SG',
# 			sum(RRSGGRADER) as 'RR_SG_GRADE',
# 			sum(GRAPHITECARBONGRANUAL) as 'GRAPHITE_CARBON_GRANUAL',
# 			sum(RESEED13MM) as 'RESEED_1_3MM',
# 			sum(FERROSILICONMAGNESIUMELMAG6225) as 'FERRO_SILICON_MAGNESIUM_ELMAG_6225',
# 			sum(FERROSILICONMAGNESIUMELMAG5800) as 'FERRO_SILICON_MAGNESIUM_ELMAG_5800'
# 		FROM (
# 			SELECT 
# 				p.name AS pouring_id, 
# 				p.heat_date AS heat_date,
# 				p.heat_no AS heat_no,
# 				c.item_code, 
# 				c.item_name, 
# 				c.quantity,
# 				CASE WHEN c.item_code = 'AFPL-RWM-009' THEN c.quantity ELSE 0 END AS MSSCRAP,
# 				CASE WHEN c.item_code = 'AFPL-RWM-006' THEN c.quantity ELSE 0 END AS CIBORING,
# 				CASE WHEN c.item_code = 'AFPL-RWM-004' THEN c.quantity ELSE 0 END AS PIGIRON,
# 				CASE WHEN c.item_code = 'AFPL-RWM-005' THEN c.quantity ELSE 0 END AS RRCIGRADE,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2682' THEN c.quantity ELSE 0 END AS CALCINEDPETROLIUMCOKE,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2676' THEN c.quantity ELSE 0 END AS FERROSILICONLUMPS,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2675' THEN c.quantity ELSE 0 END AS FERROMANGANESELUMPS,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2681' THEN c.quantity ELSE 0 END AS FERROCHROMIUMLUMPS,
# 				CASE WHEN c.item_code = 'AFPL-RWM-002' THEN c.quantity ELSE 0 END AS COPPERSCRAP,
			
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2678' THEN c.quantity ELSE 0 END AS INNOCULANTBERINOCCI,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-666' THEN c.quantity ELSE 0 END AS SLAGREMOVINGPOWDER,
# 				CASE WHEN c.item_code = 'AFPL-RWM-011' THEN c.quantity ELSE 0 END AS HEALMETAL,
# 				CASE WHEN c.item_code = 'AFPL-RWM-010' THEN c.quantity ELSE 0 END AS MSBAR,
# 				CASE WHEN c.item_code = 'AFPL-RWM-007' THEN c.quantity ELSE 0 END AS CRCSCRAP,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-665' THEN c.quantity ELSE 0 END AS SLAGHOLDINGCOMPOUND,
				
# 				CASE WHEN c.item_code = 'AFPL-RWM-003' THEN c.quantity ELSE 0 END AS PIGIRONG,
# 				CASE WHEN c.item_code = 'AFPL-RWM-001' THEN c.quantity ELSE 0 END AS RRSGGRADER,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2674' THEN c.quantity ELSE 0 END AS GRAPHITECARBONGRANUAL,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2679' THEN c.quantity ELSE 0 END AS RESEED13MM,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2683' THEN c.quantity ELSE 0 END AS FERROSILICONMAGNESIUMELMAG6225,
# 				CASE WHEN c.item_code = 'AFPL-CUNS-2685' THEN c.quantity ELSE 0 END AS FERROSILICONMAGNESIUMELMAG5800												
				
# 			FROM 
# 				`tabPouring` p 
# 			LEFT JOIN 
# 				`tabChange Mix Details` c ON p.name = c.parent 
# 			where 
# 				p.docstatus  = 1 and p.company = %s 
# 				and p.heat_date between %s and %s
# 			) x

# 			"""


# if production_item:
# 	conditions.append("wo.production_item = %s")
# 	params.append(production_item)

