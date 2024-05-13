# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def ItemWeight(item_code):
	item_weight = frappe.get_value('Production UOM Definition',{'parent': item_code ,'uom':'Kg'}, "value_per_unit")
	return item_weight if item_weight else 0

class WeightChangeJournal(Document):

	@frappe.whitelist()
	def get_item_weight(self):
		if self.item_code:
			weight = ItemWeight(self.item_code)
			self.current_weight = weight
			self.uom = 'kg'

	
	def on_update_after_submit(self):
		if self.status == 'Approved':
			self.item_master()
			self.pattern_master()


		

	@frappe.whitelist()
	def item_master(self):
		doc_name = frappe.get_value('Production UOM Definition',{'parent': self.item_code ,'uom':'Kg'}, "name")
		frappe.set_value("Production UOM Definition",doc_name,"value_per_unit", self.update_weight)


	@frappe.whitelist()
	def pattern_master(self):
		patten_id = frappe.get_all("Casting Material Details", filters = {'item_code': self.item_code}, fields = ['parent'])
		if patten_id:
			for i in patten_id:
				pattern_doc = frappe.get_doc('Pattern Master', i.parent)
				child_doc = pattern_doc.get("casting_material_details", filters={'item_code': self.item_code})
				for detail in child_doc:
					detail.weight = self.update_weight
				pattern_doc.save()