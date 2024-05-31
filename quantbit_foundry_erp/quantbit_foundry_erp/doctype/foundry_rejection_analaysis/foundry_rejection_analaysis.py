# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FoundryRejectionAnalaysis(Document):
	@frappe.whitelist()
	def get_outsourcing_job_work(self):
		 
		for i in self.get("rejection_analysis_outsourcing_job_work"):
			# frappe.msgprint(str(i.outsourcing_job_work))

			child_data=frappe.get_all("IN Rejected Items Reasons Subcontracting",filters={"parent":i.outsourcing_job_work},
							fields=["rejection_reason","name","rejection_type","raw_item_code","raw_item_name","quantity","target_warehouse",
						 		"reference_id","weight_per_unit","total_rejected_weight"])
			 
			if(child_data):
				for j in child_data:
					count=0
					for k in self.get("rejection_details"):
						if(j.name==k.child_name):
							count+=1
				
					if(count==0):
						self.append("rejection_details", {
									'rejection_reason': j.rejection_reason,
									'child_name':j.name,

									'rejection_type': j.rejection_type,
									'item_code':j.raw_item_code,

									'item_name': j.raw_item_name,
									'source_warehouse':j.target_warehouse,

									'quantity': j.quantity,
									'reference_id':i.outsourcing_job_work,

									'weight_per_unit': j.weight_per_unit,
									'total_rejected_weight':j.total_rejected_weight,

									},),
					self.get_weight_per_unit()

	@frappe.whitelist()
	def call_in_one(self):
		self.get_delivery_note()
		self.get_sales_invoice()

	@frappe.whitelist()
	def get_delivery_note(self):
		if self.customer_id:
			for i in self.get("delivery_note"):
				child_data=frappe.get_all("Delivery Note Item",filters={"parent":i.delivery_note},
								fields=["item_code","name","item_name","qty","custom_reference_id"])
				
				if(child_data):
					for j in child_data:
						self.append("rejection_details", {
									'child_name':j.name,
									'item_code':j.item_code,
									'item_name': j.item_name,
									'quantity':abs(j.qty),
									'delivery_note_ref_id':j.custom_reference_id,
									},),
				
				self.get_weight_per_unit()

	@frappe.whitelist()
	def get_sales_invoice(self):
		if self.customer_id:
			for i in self.get("sales_invoice"):
				child_data=frappe.get_all("Sales Invoice Item",filters={"parent":i.sales_invoice},
								fields=["item_code","name","item_name","qty","custom_reference_id"])
				
				if(child_data):
					for j in child_data:
						self.append("rejection_details", {

									'child_name':j.name,
									'item_code':j.item_code,
									'item_name': j.item_name,
									'quantity': abs(j.qty),
									'sales_invoice_ref_id':j.custom_reference_id,
									},),
			
				self.get_weight_per_unit()

	@frappe.whitelist()
	def get_weight_per_unit(self):
		for i in self.get("rejection_details"):
			if i.item_code:
				weight_per_unit = frappe.get_value("Production UOM Definition", filters={"parent": i.item_code, "uom": "Kg"}, fieldname="value_per_unit")
				i.weight_per_unit = weight_per_unit
				i.total_rejected_weight = float(i.weight_per_unit or 0) * float(i.quantity or 0)

	@frappe.whitelist()
	def set_filters_for_outsourcing_items(self):
		
		final_listed =[]
		doc = frappe.get_all("IN Rejected Items Reasons Subcontracting", fields =['parent'] ,filters={'docstatus': 1}, distinct='parent')
		# frappe.msgprint(str(doc))
		for d in doc:
			final_listed.append(d.parent)
		return final_listed
	
	@frappe.whitelist()
	def set_filters_for_delivery_note(self):
		final_listed = []
		doc = frappe.get_all("Delivery Note Item", 
							fields=['parent'], 
							filters={'docstatus': 1}, 
							distinct='parent')
		for d in doc:
			final_listed.append(d.parent)
		return final_listed
	
	@frappe.whitelist()
	def set_filters_for_sales_invoice(self):
		final_listed =[]
		doc = frappe.get_all("Sales Invoice Item", fields =['parent'] ,filters={'docstatus': 1},  distinct = 'parent' )
		for d in doc:
			final_listed.append(d.parent)
		return final_listed	
	
	@frappe.whitelist()
	def set_target_warehouse_item(self):
		for i in self.get('rejection_details'):
			if i.is_scrap:
				grade = frappe.get_value("Item", i.item_code,"custom_grade")
				
				if(grade):
					scrap_item = frappe.get_doc('Grade Master',grade)
					
					if scrap_item.scrap_item_code:
						i.target_warehouse_item = scrap_item.scrap_item_code
						i.scrap_item_name = scrap_item.scrap_item_name
					else:
						frappe.throw("Update Grade Master For Scrap Item")
				else:
					frappe.throw("Update Item Master For Grade")

			if not i.is_scrap:
				i.target_warehouse_item=None

	def on_submit(self):
		self.create_manufacturing_stock_entry()

	@frappe.whitelist()
	def create_manufacturing_stock_entry(self):
		for i in self.get("rejection_details" , filters= {'is_scrap': 1}):
			doc = frappe.new_doc("Stock Entry")
			doc.stock_entry_type = "Manufacture"
			doc.company = self.company
			doc.set_posting_time = True
			doc.posting_date = self.posting_date
			doc.append("items", {
				"s_warehouse": i.source_warehouse,
				"item_code": i.item_code,
				"item_name": i.item_name,
				"qty": i.quantity,
			})
			doc.append("items", {
				"t_warehouse": i.target_warehouse,
				"item_code": i.target_warehouse_item,
				"qty": i.quantity,
				"is_finished_item": True,
			})
			if self.rejection_details and doc.items:
				doc.custom_foundry_rejection_analaysis = self.name
				doc.insert()
				doc.submit()



		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = "Material Transfer"
		doc.company = self.company
		doc.set_posting_time = True
		doc.posting_date = self.posting_date
		for l in self.get("rejection_details" ,filters= {'is_scrap': 0} ):
			if l.item_code:
				doc.append("items", {
					"s_warehouse": l.source_warehouse,
					"item_code": l.item_code,
					"item_name": l.item_name,
					"qty": l.quantity,
					"t_warehouse": l.target_warehouse,
				})
		if self.rejection_details and doc.items:
			doc.custom_foundry_rejection_analaysis = self.name
			doc.insert()
			doc.submit()