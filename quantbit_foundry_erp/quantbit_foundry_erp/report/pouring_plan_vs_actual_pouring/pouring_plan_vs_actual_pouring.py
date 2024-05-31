import frappe
import calendar
import math

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    # frappe.throw(str(list(calendar.month_abbr).index("jul".capitalize())))
    return columns, data

def get_columns(filters):
    month_name = filters.get("month")
    year = int(filters.get("year"))
    month = list(calendar.month_abbr).index(month_name.capitalize())
    _, num_days = calendar.monthrange(year, month)
    columns = [
        {"fieldname": "part_name", "fieldtype": "Data", "label": "<b>Part Name</b>","width":150},
        {"fieldname": "part_code", "fieldtype": "Data", "label": "<b>Part Code</b>","width":150},
        {"fieldname": "part_no", "fieldtype": "Data", "label": "<b>Part No</b>","width":150},
        {"fieldname": "weight", "fieldtype": "Float", "label": "<b>Weight</b>","width":100},
        {"fieldname": "qty", "fieldtype": "Int", "label": "<b>Scheduled Quantity</b>","width":100},
        {"fieldname": "achievement_in_per", "fieldtype": "Float", "label": "<b>Achievement in %</b>","width":100},
        {"fieldname": "production_qty", "fieldtype": "Float", "label": "<b>Production QTY</b>","width":100},
        {"fieldname": "total_weight", "fieldtype": "Float", "label": "<b>Total Weight</b>","width":100},
        {"fieldname": "pending_qty", "fieldtype": "Float", "label": "<b>Pending QTY</b>","width":150},
        {"fieldname": "pending_weight", "fieldtype": "Float", "label": "<b>Pending Weight</b>","width":150},
        {"fieldname": "grade_type", "fieldtype": "Data", "label": "<b>Grade Type</b>","width":100},
        {"fieldname": "cavity", "fieldtype": "Int", "label": "<b>Cavity</b>","width":100},
        {"fieldname": "box_weight", "fieldtype": "Float", "label": "<b>Box Weight</b>","width":100},
        {"fieldname": "no_boxes_actual", "fieldtype": "Float", "label": "<b>No Boxes Actual</b>","width":100},
        {"fieldname": "no_boxes_heat", "fieldtype": "Float", "label": "<b>No. Boxes/Heat</b>","width":100},
        {"fieldname": "pending_heats", "fieldtype": "Float", "label": "<b>Pending Heats</b>","width":100},
        {"fieldname": "schedule_wise_heats", "fieldtype": "Float", "label": "<b>Schedule Wise Heats</b>","width":100},
        {"fieldname": "no_qty_per_heat", "fieldtype": "Float", "label": "<b>No. QTY/Heat</b>","width":100},
    ]
    week = 1
    for i in range(1, num_days + 1):
        day_of_week = calendar.weekday(year, month, i)
        if day_of_week == calendar.TUESDAY:
            columns.append({"fieldname": f"{i}_{month_name}_qty", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actqty", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_wt", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actwt", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_heat", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actheat", "fieldtype": "Data", "label": f"<b>WEEK-{week}</b>","width":150,"align":"right"})
            week += 1
        else:
            columns.append({"fieldname": f"{i}_{month_name}_qty", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actqty", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_wt", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actwt", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_heat", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})
            columns.append({"fieldname": f"{i}_{month_name}_actheat", "fieldtype": "Data", "label": f"<b>{i}-{month_name.upper()}</b>","width":100,"align":"right"})

   
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_qty", "fieldtype": "Data", "label": "","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_actqty", "fieldtype": "Data", "label": "","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_wt", "fieldtype": "Data", "label": "<b>TOTAL</b>","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_actwt", "fieldtype": "Data", "label": "","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_heat", "fieldtype": "Data", "label": "","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 1}_{month_name}_actheat", "fieldtype": "Data", "label": "","width":150,"align":"right"})
    columns.append({"fieldname": f"{num_days + 2}_{month_name}_pendingqty", "fieldtype": "Data", "label": "<b>Pending QTY</b>","width":150,"align":"right"})

    return columns


def get_data(filters):
    month_name = filters.get("month")
    year = int(filters.get("year"))
    item = filters.get("item")
    company = filters.get("company")
    month = list(calendar.month_abbr).index(month_name.capitalize())
    _, num_days = calendar.monthrange(year, month)
    full_month_name = calendar.month_name[list(calendar.month_abbr).index(month_name.capitalize())]
    
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{num_days:02d}"
    
    full_month_year = f"{full_month_name}-{year}"
   
    if not frappe.db.exists("Monthly Pouring Schedule", {"name": full_month_year, "company": company}):
        frappe.throw(f"No Monthly Data found for <strong>{full_month_name}-{year}</strong> in company <strong>{company}</strong>")

    if not frappe.db.exists("Daywise Pouring Schedule", {"name": full_month_year, "company": company}):
        frappe.throw(f"No Daily Data found for <strong>{full_month_name}-{year}</strong> in company <strong>{company}</strong>")

    month_doc = frappe.get_doc("Monthly Pouring Schedule", full_month_year)
    daywise_doc = frappe.get_doc("Daywise Pouring Schedule", full_month_year)

    data = [{}]  
    for i in range(1, num_days + 2):
        data[0][f'{i}_{month_name}_qty'] = '<b>Plan QTY</b>'
        data[0][f'{i}_{month_name}_actqty'] = '<b>Actual Quantity</b>'
        data[0][f'{i}_{month_name}_wt'] = '<b>Plan Weight</b>'
        data[0][f'{i}_{month_name}_actwt'] = '<b>Actual Weight</b>'
        data[0][f'{i}_{month_name}_heat'] = '<b>Plan Heats</b>' 
        data[0][f'{i}_{month_name}_actheat'] = '<b>Actual Heats</b>'
        
   
    item_filter = {'item_code': item} if item else None
    for j in month_doc.get("item_pouring_schedule" , filters = item_filter):

        month_production_qty,temp,month_actual_boxes = get_act_data_pouring(start_date,end_date,j.item_code)
        total_cavity_and_box_weight = frappe.db.sql("""
														SELECT b.item_code, b.qty as cavity,a.box_weight
														FROM `tabPattern Master` a
														LEFT JOIN `tabCasting Material Details` b ON a.name = b.parent
														WHERE b.item_code = %s
                                                        LIMIT 1
													""",(j.item_code),as_dict="True")
        
 
        dict = {}
        dict['part_name'] = j.item_name
        dict['part_code'] = j.item_code
        dict['part_no'] = frappe.get_value("Item",{"name":j.item_code},"custom_part_number")
        dict['weight'] = j.weight_per_unit_quantity if j.weight_per_unit_quantity else 0
        dict['qty'] = j.schedule_quantity if j.schedule_quantity else 0
        dict['grade_type'] = frappe.get_value("Grade Master",frappe.get_value("Item",{"name":j.item_code},"custom_grade"),"grade_type")
        dict['production_qty'] = month_production_qty
        dict['total_weight'] =  (dict['production_qty']) * (dict['weight'])
        dict['achievement_in_per'] =  (dict['production_qty']/j.schedule_quantity)*100 
        dict['pending_qty'] = j.schedule_quantity - dict['production_qty']
        dict['pending_weight'] = dict['pending_qty']*dict['weight']
        dict['cavity'] =  total_cavity_and_box_weight[0]['cavity'] if total_cavity_and_box_weight and total_cavity_and_box_weight[0]['cavity'] else 0
        dict['box_weight'] =  total_cavity_and_box_weight[0]['box_weight'] if total_cavity_and_box_weight and total_cavity_and_box_weight[0]['box_weight'] else 0
        dict['no_boxes_actual'] = month_actual_boxes
        dict['no_boxes_heat'] = 500 / dict['box_weight'] if dict['box_weight'] else 0
        dict['no_qty_per_heat'] = dict['cavity']*dict['no_boxes_heat']
        dict['pending_heats'] = math.ceil(dict['pending_qty']/dict['no_qty_per_heat']) if dict['no_qty_per_heat'] else 0
        dict['schedule_wise_heats'] = math.ceil(dict['qty']/dict['no_qty_per_heat']) if dict['no_qty_per_heat'] else 0
        
      
        
        week_qty = week_wt = weak_heat = week_actqty = week_actheat = week_actwt = 0
        total_week_qty = total_week_wt = total_week_heat = total_week_actqty = total_week_actheat = total_week_actwt = 0
        for k in daywise_doc.get("item_pouring_schedule", filters = {'item_code': j.item_code}):
            m = (int(str(k.planning_date)[-2:])) # get last two digits of date for dictionary key
            day_of_week = calendar.weekday(year, month, m)
            if day_of_week != calendar.TUESDAY:
                act_production_qty , act_heat,temp = get_act_data_pouring(k.planning_date , k.planning_date , j.item_code)
                
                
                dict[f"{m}_{month_name}_qty"] = k.planned_quantity
                dict[f"{m}_{month_name}_wt"] = k.planned_weight
                dict[f"{m}_{month_name}_heat"] = k.planed_pouring_count   
                dict[f"{m}_{month_name}_actqty"] = act_production_qty if act_production_qty else 0
                dict[f"{m}_{month_name}_actheat"] = act_heat if act_heat else 0
                dict[f"{m}_{month_name}_actwt"] = f"{round(dict['weight'] * act_production_qty if act_production_qty else 0, 3):.3f}"
                # dict[f"{m}_{month_name}_actwt"] = (dict['weight']*act_production_qty if act_production_qty else 0.000)
                # dict[f"{m}_{month_name}_actwt"] = round((dict['weight']*act_production_qty if act_production_qty else 0),3)
                
                week_qty +float(k.planned_quantity)
                week_wt += float(k.planned_weight)
                weak_heat += float(k.planed_pouring_count)
                week_actqty += act_production_qty if act_production_qty else 0
                week_actheat += act_heat if act_heat else 0
                week_actwt += dict['weight']*act_production_qty if act_production_qty else 0
                
                total_week_qty += float(k.planned_quantity)
                total_week_wt += float(k.planned_weight)
                total_week_heat += float(k.planed_pouring_count)
                total_week_actqty+=act_production_qty if act_production_qty else 0
                total_week_actheat+=act_heat if act_heat else 0
                total_week_actwt += dict['weight']*act_production_qty if act_production_qty else 0
            else:
                dict[f"{m}_{month_name}_qty"] = f"{week_qty:.3f}"
                dict[f"{m}_{month_name}_wt"] = f"{week_wt:.3f}"
                dict[f"{m}_{month_name}_heat"] = f"{weak_heat:.3f}"
                dict[f"{m}_{month_name}_actqty"] = f"{week_actqty:.3f}"
                dict[f"{m}_{month_name}_actheat"] = f"{week_actheat:.3f}"
                dict[f"{m}_{month_name}_actwt"] = f"{week_actwt:.3f}"
                week_qty = week_wt = weak_heat = week_actqty = week_actheat = week_actwt = 0
                
        dict[f"{num_days+1}_{month_name}_qty"] = f"{total_week_qty:.3f}"
        dict[f"{num_days+1}_{month_name}_wt"] = f"{total_week_wt:.3f}"
        dict[f"{num_days+1}_{month_name}_heat"] = f"{total_week_heat:.3f}"
        dict[f"{num_days+1}_{month_name}_actqty"] = f"{total_week_actqty:.3f}"
        dict[f"{num_days+1}_{month_name}_actheat"] = f"{total_week_actheat:.3f}"
        dict[f"{num_days+1}_{month_name}_actwt"] = f"{total_week_actwt:.3f}"
        dict[f"{num_days+2}_{month_name}_pendingqty"] = dict['pending_qty']
        # frappe.msgprint(str(dict))
               
        data.append(dict)
    
    # Total Sum    
    # dict1 = {}
    
    # dict1['part_name'] = "Total"
    # dict1['weight'] =sum(data[i]['weight'] for i in range(1,len(data)))
    # dict1['qty'] =sum(data[i]['qty'] for i in range(1,len(data)))
    # dict1['achievement_in_per'] =sum(data[i]['achievement_in_per'] for i in range(1,len(data)))
    # dict1['production_qty'] =sum(data[i]['production_qty'] for i in range(1,len(data)))
    # dict1['total_weight'] =sum(data[i]['total_weight'] for i in range(1,len(data)))
    # dict1['pending_qty'] =sum(data[i]['pending_qty'] for i in range(1,len(data)))
    # dict1['pending_weight'] =sum(data[i]['pending_weight'] for i in range(1,len(data)))
    # dict1['cavity'] =sum(data[i]['cavity'] for i in range(1,len(data)))
    # dict1['box_weight'] =sum(data[i]['box_weight'] for i in range(1,len(data)))
    # dict1['no_boxes_actual'] =sum(data[i]['no_boxes_actual'] for i in range(1,len(data)))
    # dict1['no_boxes_heat'] =sum(data[i]['no_boxes_heat'] for i in range(1,len(data)))
    # dict1['pending_heats'] =sum(data[i]['pending_heats'] for i in range(1,len(data)))
    # dict1['schedule_wise_heats'] =sum(data[i]['schedule_wise_heats'] for i in range(1,len(data)))
    # dict1['no_qty_per_heat'] =sum(data[i]['no_qty_per_heat'] for i in range(1,len(data)))
    # # frappe.msgprint(str(data[0]))
    # for j in range(1,num_days+1):
    #     dict1[f"{j}_{month_name}_qty"] = sum(float(data[i][f"{j}_{month_name}_qty"]) for i in range(1, len(data)) if f"{j}_{month_name}_qty" in data[i])
    #     dict1[f"{j}_{month_name}_wt"] = sum(float(data[i][f"{j}_{month_name}_wt"]) for i in range(1, len(data)) if f"{j}_{month_name}_wt" in data[i])
    #     dict1[f"{j}_{month_name}_heat"] =  sum(float(data[i][f"{j}_{month_name}_heat"]) for i in range(1, len(data)) if f"{j}_{month_name}_heat" in data[i])  
    #     dict1[f"{j}_{month_name}_actqty"] =  sum(float(data[i][f"{j}_{month_name}_actqty"]) for i in range(1, len(data)) if f"{j}_{month_name}_actqty" in data[i])
    #     dict1[f"{j}_{month_name}_actheat"] =  sum(float(data[i][f"{j}_{month_name}_actheat"]) for i in range(1, len(data)) if f"{j}_{month_name}_actheat" in data[i])
    #     dict1[f"{j}_{month_name}_actwt"] = sum(float(data[i][f"{j}_{month_name}_actwt"]) for i in range(1, len(data)) if f"{j}_{month_name}_actwt" in data[i])
    # data.append(dict1)

        
   
    return data


def get_act_data_pouring(from_date , to_date , item_code):
    total_qty_of_items = frappe.db.sql("""
														SELECT b.item_code, SUM(b.total_quantity) as production_qty,count(a.name) as heat,(b.total_quantity/b.quantitybox) as actual_boxes
														FROM `tabPouring` a
														LEFT JOIN `tabCasting Details` b ON a.name = b.parent
														WHERE a.heat_date BETWEEN %s AND %s AND b.item_code = %s AND a.docstatus=1
													""",(from_date , to_date, item_code),as_dict="True")
    
    production_qty = total_qty_of_items[0]['production_qty'] if total_qty_of_items and total_qty_of_items[0]['production_qty'] else 0
    heat = total_qty_of_items[0]['heat'] if total_qty_of_items and total_qty_of_items[0]['heat'] else 0
    actual_boxes = total_qty_of_items[0]['actual_boxes'] if total_qty_of_items and total_qty_of_items[0]['actual_boxes'] else 0 
    return production_qty , heat, actual_boxes

