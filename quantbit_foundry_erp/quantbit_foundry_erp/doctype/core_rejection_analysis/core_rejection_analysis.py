# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CoreRejectionAnalysis(Document):
	def on_submit(self):
		self.create_material_issue_stock_entry()

	@frappe.whitelist()
	def create_material_issue_stock_entry(self):
		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = "Material Issue"
		doc.company = self.company
		doc.set_posting_time = True
		doc.posting_date =self.transaction_date

		for i in self.get("core_rejection_details"):
			doc.append("items", {
				"s_warehouse": i.core_warehouse,
				"item_code": i.core_item_code,
				"item_name": i.core_item_name,
				"qty": i.core_rejection_quantity,
			})
		if self.core_rejection_details:
			doc.custom_core_rejection_analysis = self.name
			doc.insert()
			doc.submit()