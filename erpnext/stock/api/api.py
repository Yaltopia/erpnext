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

@frappe.whitelist()
def create_buying_item_price():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock_repriced.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item_price_id = frappe.db.get_value("Item Price", {"item_code": row[0], "price_list": "Standard Buying"}, "name")
			if item_price_id:
				item_price = frappe.get_doc("Item Price", item_price_id)
				item_price.price_list_rate = row[8]
				item_price.save()
			else:
				item_price = frappe.new_doc("Item Price")
				item_price.item_code = row[0]
				item_price.price_list = 'Standard Buying'
				item_price.price_list_rate = row[8]
				item_price.currency = 'ETB'
				item_price.save()
		frappe.db.commit()
		return True

@frappe.whitelist()
def create_purchase_order ():
	# get csv files that have the word repriced in their name from the directory
	purchase_orders = []
	for file in os.listdir('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/'):
		if file.endswith(".csv"):
			if file.find('repriced') == -1:
				continue

			print(os.path.join("/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/", file))
			csvfile = open(os.path.join("/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/", file))
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			purchase_order = frappe.new_doc("Purchase Order")
			purchase_order.append("taxes", {
				"charge_type": "On Net Total",
				"account_head": "VAT - YT",
				"description": "VAT 15% on Purchase",
				"rate": 15,
				"add_deduct_tax": "Add"
			})
			total_amount = 0
			total_weight = 0
			total_quantity = 0
			for row in spamreader:
				if row[0] == 'Supplier':
					purchase_order.supplier =  row[1]
					purchase_order.transaction_date = row[3]
					purchase_order.schedule_date = row[3]
					continue

				item = frappe.db.get_value("Item", {"item_code": row[0]})

				if item:
					item_doc = frappe.get_doc("Item", item)
					purchase_order.append("items", {
						"item_code": row[0],
						"schedule_date": purchase_order.schedule_date,
						"uom": "Nos",
						"qty": row[7],
						"rate": row[8],
						# "weight_per_unit": item_doc.weight_per_unit,
						# "total_weight": float (row[7]) * item_doc.weight_per_unit,
						"amount": float (row[7]) * float (row[8]),
						"net_amount": float (row[7]) * float (row[8]),
						"base_net_amount": float (row[7]) * float (row[8]),
						"base_amount": float (row[7]) * float (row[8]),
						"base_rate": float (row[8]),
						"base_total": float (row[7]) * float (row[8]),


					})
					total_amount = total_amount + float (row[7]) * float (row[8])
					total_weight = total_weight + float (row[7]) * item_doc.weight_per_unit
					total_quantity = total_quantity + float (row[7])
			purchase_order.net_total = total_amount
			purchase_order.total_net_weight = total_weight
			purchase_order.total_qty = total_quantity

			purchase_order.set_missing_values()
			purchase_orders.append(purchase_order)
			# recalculates taxes and totals
			purchase_order.save()
	return purchase_orders

