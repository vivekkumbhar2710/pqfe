# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DaywisePouringSchedule(Document):
	def before_save(self):
		self.set_wpu_and_weight()

	def set_wpu_and_weight(self):
		total_qty = 0
		total_weight = 0
		for i in self.get("item_pouring_schedule"):
			item_weight = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
			i.weight_per_unit_quantity =  item_weight if item_weight else 0
			i.planned_weight = i.weight_per_unit_quantity * i.planned_quantity
			total_qty+=i.planned_quantity
			total_weight+=i.planned_weight

		self.total_quantity = total_qty
		self.total_weight = total_weight
	@frappe.whitelist()
	def get_patterns(self,item_code):
		patterns = frappe.db.sql("""
														SELECT a.name
														FROM `tabPattern Master` a
														LEFT JOIN `tabCasting Material Details` b ON a.name = b.parent
														WHERE b.item_code = %s
													""",(item_code),as_dict="True")
		pattern_list = [i['name'] for i in patterns]
		return pattern_list
     
	# @frappe.whitelist()
	# def set_total_weight(self,date):
	# 	data = self.get("item_pouring_schedule",filters={"planning_date":date})
	# 	self.daywise_total_weight = sum(i.planned_weight if i.planned_weight else 0 for i in data)
		
		
     