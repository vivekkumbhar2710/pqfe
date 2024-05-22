# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PurchaseMaterialReturn(Document):

    
	@frappe.whitelist()
	def get_rate(self):
		for i in self.get("material_return"):
			if i.purchase_order:
				rate = frappe.get_value("Purchase Order Item",{'parent': i.purchase_order,"item_code": i.item},"rate")
				if rate:
					i.rate = rate
				else:	
					i.rate = None
					frappe.msgprint(f"<strong>{i.item}</strong> Item Doesn't Exists in <strong>{i.purchase_order}</strong>")
					return
					
					
    
	@frappe.whitelist()
	def get_available_qty(self):
		for i in self.get('material_return'):
			if i.source_warehouse:
				if frappe.db.exists("Bin",{"warehouse":i.source_warehouse,"item_code":i.item}):
					qty = frappe.get_value("Bin",{"warehouse":i.source_warehouse,"item_code":i.item},'actual_qty')
					i.available_quantity = qty
				else:
					i.available_quantity = None
					frappe.msgprint(f"<strong>{i.item}</strong> Item not found in <strong>{i.source_warehouse}</strong>")
					i.source_warehouse = None
					# return frappe.get_meta("Purchase Material Return").get_custom_fields()
					
          
	def on_submit(self):
		self.material_issue_stock_entry() 
  
	@frappe.whitelist()
	def material_issue_stock_entry(self):
		doc = frappe.new_doc("Stock Entry")
		doc.set_posting_time = True
		doc.posting_date = self.date
		doc.custom_purchase_material_return = self.name
		doc.stock_entry_type = "Purchase Material Return"
		doc.company = self.company
  
		for i in self.get("material_return"):
			doc.append("items",{
				"s_warehouse":i.source_warehouse,
				"item_code":i.item,
				"qty":i.quantity,

			})
		doc.insert()
		doc.save()
		doc.submit()
	

		
		
		
		
  

			

		
