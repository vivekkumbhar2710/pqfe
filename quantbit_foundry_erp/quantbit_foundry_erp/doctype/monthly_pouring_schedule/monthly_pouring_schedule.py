# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyPouringSchedule(Document):
    def before_save(self):
        self.set_wpu_and_total_weight()
    
    def set_wpu_and_total_weight(self):
        total_qty = 0
        total_weight = 0
        for i in self.get("item_pouring_schedule"):
            item_weight = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
            i.weight_per_unit_quantity =  item_weight if item_weight else 0
            i.total_weight = i.weight_per_unit_quantity * i.schedule_quantity
            total_qty += i.schedule_quantity
            total_weight += i.total_weight
        self.total_quantity = total_qty
        self.total_weight = total_weight
