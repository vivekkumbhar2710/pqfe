# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def getVal(val):
	return val if val is not None else 0

 
class MaterialConversion(Document):

	def before_save(self):
		self.call_method()

	@frappe.whitelist()
	def get_available_quantity_input_material(self):
		input_material = self.get("input_material")
		for row in input_material : 
			if row.warehouse :
				actual_qty = frappe.get_value('Bin',{'item_code':row.item_code,"warehouse":row.warehouse},'actual_qty')
				if actual_qty :
					row.available_quantity = actual_qty
				else :
					frappe.msgprint("The Available Quantity for this item in the warehouse is not available.")
					row.warehouse = None 
      
	@frappe.whitelist()
	def get_available_quantity_output_material(self):
		output_material = self.get("output_material")
		for row in output_material : 
			if row.warehouse :
				actual_qty = frappe.get_value('Bin',{'item_code':row.item_code,"warehouse":row.warehouse},'actual_qty')
				if actual_qty :
					row.available_quantity = actual_qty
				
	@frappe.whitelist()
	def get_value_per_unit_for_input(self):
		input_material = self.get("input_material")
		for i in input_material:
			if i.item_code:
				value = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
				i.weight_per_unit = value if value else 0

	@frappe.whitelist()
	def get_value_per_unit_for_output(self):
		output_material = self.get("output_material")
		for i in output_material:
			if i.item_code:
				value = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
				i.weight_per_unit = value if value else 0

	@frappe.whitelist()  
	def total_weight_on_input_material(self):
		input_material = self.get("input_material") 
		for row in input_material:
			total_weight = getVal(row.quantity) * getVal(row.weight_per_unit)
			row.total_weight = total_weight
		
		self.call_method()
	
	@frappe.whitelist()  
	def total_weight_on_output_material(self):
		output_material = self.get("output_material") 
		for row in output_material:
			total_weight = getVal(row.quantity) * getVal(row.weight_per_unit)
			row.total_weight = total_weight
		
	@frappe.whitelist()
	def call_method(self):
		self.input_total_quantity = self.calculating_total('input_material','quantity')	
		self.input_total_weight_conversion = self.calculating_total('input_material','total_weight')	
 
	@frappe.whitelist()
	def call_method_output(self):
		self.total_weight_on_output_material()
		#frappe.msgprint("Hii in Output Material")
		self.output_total_quantity = self.calculating_total('output_material','quantity')
		self.output_total_weight_conversion = self.calculating_total('output_material','total_weight')	

	@frappe.whitelist()
	def calculating_total(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = getVal(i.get(total_field))
			total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight
 
	@frappe.whitelist()
	def validate_stock_entry(self):
		for i in self.get("input_material"):
			qty = 0
			for j in self.get("output_material"):
				if i.item_code == j.posting_item_code:
					qty+=j.quantity
			if qty != i.quantity:
				frappe.throw(f"<strong>{i.item_code}</strong> Input Quantity doesn't match with Output Quantity")
				return False
		return True	

	def on_submit(self):
		self.Manufacturing_stock_entry()
	def before_save(self):
		self.validate_stock_entry()
 
	# After Submitting Component Work Order Manufacturing Stock Entry will be created 
	@frappe.whitelist()
	def Manufacturing_stock_entry(self):
	
		if self.validate_stock_entry():
			for i in self.get("input_material"):
				for j in self.get("output_material"):
					if i.item_code == j.posting_item_code:
						doc = frappe.new_doc("Stock Entry")
						doc.stock_entry_type = "Manufacture"
						doc.company = self.company
						doc.set_posting_time = True
						doc.posting_date =self.posting_date
      
						doc.append("items", {
						"s_warehouse": i.warehouse,
						"item_code": i.item_code,
						"qty": i.quantity,
						})

					
						doc.append("items", {
						"t_warehouse": j.warehouse,
						"item_code": j.item_code,
						"qty": j.quantity,
						"is_finished_item": True,
						})
			
						doc.insert()
						doc.save()
						doc.submit()
		
		
			# doc = frappe.new_doc("Stock Entry")
		# doc.stock_entry_type = "Manufacture"
		# doc.company = self.company
		# doc.set_posting_time = True
		# doc.posting_date =self.posting_date

		# for i in self.get("input_material"):
		# 	doc.append("items", {
		# 		"s_warehouse": i.warehouse,
		# 		"item_code": i.item_code,
		# 		"qty": i.quantity ,
		# 	})
		
		# for i in self.get("output_material"):
		# 	doc.append("items", {
		# 		"t_warehouse": i.warehouse,
		# 		"item_code": i.item_code,
		# 		"qty": i.quantity,
		# 		"is_finished_item": True,
		# 	})
		# flag = 0
		# inp_mat_dict = {}
		# set_out_mat = {}
		# for i in self.get("input_material"):
		# 	inp_mat_dict[i.item_code] = i.quantity

		# for i in self.get("output_material"):
		# 	if i.posting_item_code in set_out_mat:
		# 		set_out_mat[i.posting_item_code] += i.quantity
		# 	else:
		# 		set_out_mat[i.posting_item_code] = i.quantity
    
		# for item_code, quantity_in in inp_mat_dict.items():
		# 	if item_code in set_out_mat:
		# 		quantity_out = set_out_mat[item_code]
		# 		if quantity_in == quantity_out:
		# 			flag = 0
		# 		else:
		# 			frappe.throw("Input and Output Quantities doesn't match")
