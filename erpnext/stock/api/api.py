import frappe
import csv
import os

@frappe.whitelist(allow_guest=True)
def test_csv():
	print(os.getcwd())
	with open ('/home/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			print (row)
		return str(spamreader)

@frappe.whitelist()
def add_item_templates_to_system():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item_template = frappe.new_doc("Item")
			item_template.item_code =  row[0]
			item_template.item_group =  str(row[1])
			item_template.item_name =  row[7]
			item_template.allow_alternative_item = 1
			item_template.stock_uom =  'Nos'
			item_template.attributes = [frappe.get_doc({
				'doctype' : "Item Variant Attribute",
				'attribute': "Weight",
				'variant_of': None,
				'attribute': 'Weight',
				'attribute_value': None,
				'numeric_values': 1,
				'from_range': 0.0,
				'increment': 0.001,
				'to_range': 100.0,
				'parent': row[0],
				'parentfield': 'attributes',
				'parenttype': 'Item',
			})]
			item_template.variant_based_on = 'Item Attribute'
			item_template.weight_uom = 'Kg'
			item_template.price_per_kg = float (row[5])
			item_template.has_variants = 1

			item_template.insert()
			# weight_attribute.insert()


		frappe.db.commit()
		return True

@frappe.whitelist()
def add_item_varients_to_system():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item_varient = frappe.new_doc("Item")
			item_varient.item_name = row[7]
			item_varient.has_variants = 0
			item_varient.item_code = str(row[0]) + '-' + row[3]
			item_varient.variant_of = row[0]
			item_varient.attributes = [frappe.get_doc({
				'doctype' : "Item Variant Attribute",
				'attribute': "Weight",
				'variant_of': row[0],
				'attribute': 'Weight',
				'attribute_value': row[3],
				'parent': str(row[0]) + '-' + row[3],
				'parentfield': 'attributes',
				'parenttype': 'Item',
			})]
			item_varient.item_group = row[1]
			item_varient.allow_alternative_item = 1
			item_varient.weight_per_unit = row[3]
			item_varient.standard_rate = row[6]
			item_varient.valuation_rate = row[6]
			item_varient.insert()

			item_varient_2 = frappe.new_doc("Item")
			item_varient_2.item_name = row[7]
			item_varient_2.has_variants = 0
			item_varient_2.item_code = str(row[0]) + '-' + row[8]
			item_varient_2.allow_alternative_item = 1
			item_varient_2.variant_of = row[0]
			item_varient_2.attributes = attributes = [frappe.get_doc({
				'doctype' : "Item Variant Attribute",
				'attribute': "Weight",
				'variant_of': row[0],
				'attribute_value': row[8],
				'parent': str(row[0]) + '-' + row[8],
				'parentfield': 'attributes',
				'parenttype': 'Item',
			})]
			item_varient_2.item_group = row[1]
			item_varient_2.weight_per_unit = row[8]
			item_varient_2.standard_rate = row[9]
			item_varient_2.valuation_rate = row[9]
			item_varient_2.insert()
		frappe.db.commit()
		return True

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
def modify_item_alternative_settings():
	with open ('/home/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			item_template = frappe.get_doc ("Item", row[0])
			item_template.allow_alternative_item = 1
			item_template.save()
			frappe.db.commit()


@frappe.whitelist()
def check_item():
	items = frappe.get_all("Item Variant Attribute")
	print (items)
	for item in items:
		item_doc = frappe.get_doc('Item Variant Attribute', item.name).as_dict()
		print (str(item_doc))
	#     item_doc.delete()
	# frappe.db.commit()

def sort_sle_entries_by_creation_date (sles):
	if len(sles) > 1:
		mid = len(sles)//2
		L = sles[:mid]
		R = sles[mid:]
		sort_sle_entries_by_creation_date(L)
		sort_sle_entries_by_creation_date(R)
		i = j = k = 0
		while (i < len(L) and j < len(R)):
			if (L[i].creation > R[j].creation):
				sles[k] = L[i]
				i += 1
			else:
				sles[k] = R[j]
				j += 1
			k += 1
		while (i < len(L)):
			sles[k] = L[i]
			i += 1
			k += 1
		while (j < len(R)):
			sles[k] = R[j]
			j += 1
			k += 1
	return sles

@frappe.whitelist()
def get_stock_ledger_entries_for_item(item_code):
	entries = frappe.get_all("Stock Ledger Entry", filters={
		"item_code": item_code
	})
	entry_doc_list = []
	for entry in entries:
		entry_doc = frappe.get_doc ("Stock Ledger Entry", entry.name)
		entry_doc_list.append (entry_doc)

	return sort_sle_entries_by_creation_date(entry_doc_list)

@frappe.whitelist()
def get_last_stock_ledger_entry_for_item (item_code):
	entry_doc = frappe.get_last_doc ("Stock Ledger Entry", filters= {
		'item_code' : item_code
	}).as_dict()
	return entry_doc

@frappe.whitelist()
def create_item_varients_alternatives():
	with open ('/Users/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			varient_1 = frappe.get_doc ("Item", str(row[0]) + '-' + row[3])
			varient_2 = frappe.get_doc ("Item", str(row[0]) + '-' + row[8])

			item_alternative = frappe.new_doc ("Item Alternative")
			item_alternative.item_code = varient_1.item_code
			item_alternative.alternative_item_code = varient_2.item_code
			item_alternative.two_way = 1
			item_alternative.item_name = varient_1.item_name
			item_alternative.alternative_item_name = varient_2.item_name
			item_alternative.insert()
		frappe.db.commit()

@frappe.whitelist()
def get_item_alternative (item_code):
	item_alternative = frappe.get_all("Item Alternative", filters= {
		'item_code' : item_code
	})

	if (len(item_alternative) == 0):
		item_alternative = frappe.get_all ("Item Alternative", filters={
			"alternative_item_code" : item_code
		})

	item_alternative_doc = frappe.get_doc ("Item Alternative", item_alternative[0].name)

	alternate_item_code = ""
	if (item_code == item_alternative_doc.item_code ):
		alternate_item_code = item_alternative_doc.alternative_item_code
	else :
		alternate_item_code = item_alternative_doc.item_code

	return frappe.get_doc ("Item", alternate_item_code)

@frappe.whitelist()
def check_alternative_stock (item_code, warehouse):
	alternative = get_item_alternative (item_code)
	from erpnext.stock.doctype.quick_stock_balance.quick_stock_balance import get_stock_item_details

	alternate_stock_balance = get_stock_item_details (item = alternative.item_code, warehouse=warehouse)
	return alternate_stock_balance

@frappe.whitelist()
def cancel_purchase(purchase_receipt):
	purchase_receipt_doc = frappe.get_doc ("Purchase Receipt", purchase_receipt)
	# cancel purchase receipt
	if purchase_receipt_doc.docstatus == 1:
		pass
	# else:
	# 	return

	purchase_orders = []
	for item in purchase_receipt_doc.items:
		if item.purchase_order not in purchase_orders:
			purchase_orders.append (item.purchase_order)

	# get purchase invoices
	purchase_invoices = []
	purchase_invoices_all = frappe.get_all ("Purchase Invoice", filters={
		"docstatus" : 1
	})
	for purchase_invoice in purchase_invoices_all:
		purchase_invoice_doc = frappe.get_doc ("Purchase Invoice", purchase_invoice.name)
		if purchase_invoice_doc.items[0].purchase_order in purchase_orders and purchase_invoice.name not in purchase_invoices:
			purchase_invoices.append (purchase_invoice.name)

	# cancel purchase invoices
	for purchase_invoice in purchase_invoices:
		purchase_invoice_doc = frappe.get_doc ("Purchase Invoice", purchase_invoice)
		if purchase_invoice_doc.docstatus == 1:
			purchase_invoice_doc.cancel()

	# cancel purchase receipt
	purchase_receipt_doc = frappe.get_doc ("Purchase Receipt", purchase_receipt)
	if purchase_receipt_doc.docstatus == 1:
		purchase_receipt_doc.cancel()

	# cancel purchase orders
	for purchase_order in purchase_orders:
		purchase_order_doc = frappe.get_doc ("Purchase Order", purchase_order)
		if purchase_order_doc.docstatus == 1:
			purchase_order_doc.cancel()

	# create list of items
	return purchase_receipt_doc.items

@frappe.whitelist()
def create_purchase_test():
	items = [
		{
			"item_code" : "CP01-5.176",
			"qty" : 1
		}
	]
	warehouse = "YalHouse - YT"
	supplier = "Absolute Supplier"
	date = "2023-07-17"

	return create_purchase (items, warehouse, supplier, date)

def create_purchase (items, warehouse, supplier, date):
	# create purchase order
	purchase_order_doc = frappe.new_doc ("Purchase Order")
	purchase_order_doc.supplier = supplier
	purchase_order_doc.schedule_date = date
	# purchase_order_doc.conversion_rate = 1.0
	for item in items:
		purchase_order_doc.append ("items", {
			"item_code" : item["item_code"],
			"warehouse" : warehouse,
			"qty" : item["qty"],
			"schedule_date" : date,
			"price_list_rate": item["price_list_rate"],
			"last_purchase_rate": item["last_purchase_rate"],
			"base_price_list_rate": item["base_price_list_rate"],
			"margin_type": item["margin_type"],
			"margin_rate_or_amount": item["margin_rate_or_amount"],
			"rate_with_margin": item["rate_with_margin"],
			"discount_percentage": item["discount_percentage"],
			"discount_amount": item["discount_amount"],
			"base_rate_with_margin": item["base_rate_with_margin"],
			"rate": item["rate"],
			"amount": item["amount"],
			"base_rate": item["base_rate"],
			"base_amount": item["base_amount"],
			"stock_uom_rate": item["qty"],
			"is_free_item": item["is_free_item"],
			"apply_tds": item["apply_tds"],
			"net_rate": item["net_rate"],
			"net_amount": item["net_amount"],
			"base_net_rate": item["base_net_rate"],
			"base_net_amount": item["base_net_amount"],
			"warehouse": "YalHouse - YT",
			"delivered_by_supplier": item["delivered_by_supplier"],
			"against_blanket_order": item["against_blanket_order"],
			"blanket_order_rate": item["blanket_order_rate"],
			"billed_amt": item["billed_amt"],
			"expense_account": "Cost of Goods Sold - YT",
		})
	purchase_order_doc
	# purchase_order_doc.validate()
	from erpnext.buying.doctype.purchase_order.purchase_order import set_missing_values
	# set_missing_values(purchase_order_doc.name, purchase_order_doc)

	purchase_order_doc.insert()
	purchase_order_doc.submit()

	# create purchase receipt
	from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
	purchase_receipt_doc = make_purchase_receipt(purchase_order_doc.name)
	purchase_receipt_doc.insert()
	purchase_receipt_doc.submit()

	# purchase_receipt_doc = frappe.new_doc ("Purchase Receipt")
	# purchase_receipt_doc.supplier = supplier

	# for item in items:
	# 	purchase_receipt_doc.append ("items", {
	# 		"item_code" : item["item_code"],
	# 		"warehouse" : warehouse,
	# 		"qty" : item["qty"],
	# 		"purchase_order" : purchase_order_doc.name
	# 	})
	# purchase_receipt_doc.insert()
	# purchase_receipt_doc.submit()

	# create purchase invoice
	from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice
	purchase_invoice_doc = make_purchase_invoice(purchase_receipt_doc.name)
	purchase_invoice_doc.insert()
	purchase_invoice_doc.submit()

	frappe.db.commit()
	# purchase_invoice_doc = frappe.new_doc ("Purchase Invoice")
	# purchase_invoice_doc.supplier = supplier
	# for item in items:
	# 	purchase_invoice_doc.append ("items", {
	# 		"item_code" : item["item_code"],
	# 		"warehouse" : warehouse,
	# 		"qty" : item["qty"],
	# 		"purchase_order" : purchase_order_doc.name,
	# 		"purchase_receipt" : purchase_receipt_doc.name
	# 	})
	# purchase_invoice_doc.insert()
	# purchase_invoice_doc.submit()





@frappe.whitelist()
def obtain_stock_from_variant (item_code, warehouse, quantity):
	# validate quantity
	# for Nos for now
	if (quantity <= 0):
		frappe.throw (
			"Quantity must be a positive value "
		)
		return
	if (quantity % 1 != 0):
		print ("check")
		frappe.throw (
			"Quantity for Nos must be an Intiger "
		)
		return
	# check_alternative_stock first
	alternate_stock = check_alternative_stock (item_code, warehouse)
	print (alternate_stock)
	if (float(alternate_stock["qty"]) < quantity ):
		frappe.throw (
			"Variant Quantity not sufficient for Stock Conversion"
		)
		return
	alternate_item = get_item_alternative (item_code)
	print (alternate_item.item_code)
	sles = get_stock_ledger_entries_for_item (item_code=alternate_item.item_code)
	print (len(sles))
	# return sles
	for sle in sles:
		if (sle.actual_qty > quantity):
			canceled_items = None
			supplier = None
			if (sle.voucher_type == "Purchase Receipt"):
				purchase_receipt = frappe.get_doc ("Purchase Receipt", sle.voucher_no)
				supplier = purchase_receipt.supplier
				if (purchase_receipt.docstatus == 1):
					canceled_items = cancel_purchase (sle.voucher_no)

			#modyfy canceled items
			if (canceled_items != None):
				alter_item_template = {}
				for item in canceled_items:
					if (item.item_code == alternate_item.item_code):
						alter_item_template = item.as_dict()
						item.qty = item.qty - quantity
						break
				canceled_items_dict = []
				for item in canceled_items:
					canceled_items_dict.append (item.as_dict())
				alter_item_template["qty"] = quantity
				alter_item_template["item_code"] = item_code
				canceled_items_dict.append(alter_item_template)
				import datetime
				date = datetime.datetime.now().date()
				create_purchase (canceled_items_dict, warehouse, supplier, date=date)
