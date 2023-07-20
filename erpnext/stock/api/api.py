import frappe
import csv
import os

@frappe.whitelist()
def add_items_to_system():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item = frappe.new_doc("Item")
			item.item_code =  row[0]
			item.item_group =  str(row[1])
			item.item_name =  row[7]
			item.stock_uom =  'Nos'
			item.weight_uom = 'Kg'
			item.price_per_kg = float (row[5])
			item.has_variants = 0
			item.weight_per_unit = row[3]
			item.standard_rate = row[6]
			item.weight_per_unit_v2 = row[8]
			item.standard_rate_v2 = row[9]

			item.insert()
		frappe.db.commit()
		return True

@frappe.whitelist()
def create_purchase_order():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			purchase_order = frappe.new_doc("Purchase Order")
			purchase_order.supplier =  row[2]
			purchase_order.company = 'Eco Green'
			purchase_order.currency = 'ETB'
			purchase_order.schedule_date = '2018-02-01'
			purchase_order.set_posting_time = 1
			purchase_order.set_warehouse = 1
			purchase_order.taxes_and_charges = 'VAT 15% on Purchase'
			purchase_order.taxes = 'VAT 15% on Purchase'
			purchase_order.items = [
				{
					"item_code": row[0],
					"item_name": row[7],
					"description": row[7],
					"uom": "Nos",
					"qty": row[4],
					"rate": row[6],
					"amount": row[6]
				}
			]
			purchase_order.insert()
		frappe.db.commit()
		return True

@frappe.whitelist()
def update_item_pricing ():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock_repriced.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item = frappe.get_doc("Item", row[0])
			item.price_per_kg = float (row[10])
			item.save()
		frappe.db.commit()
		return True
