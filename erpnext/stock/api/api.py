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
    with open ('/home/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
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
    with open ('/home/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
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

# def cancel_purchase_order():
#     order = frappe.get_last_doc("Purchase Order")
#     order.run_method('cancel')
#     frappe.db.commit()

@frappe.whitelist()
def create_item_varients_alternatives():
    with open ('/home/yaredgd/frappe-bench/apps/erpnext/erpnext/stock/api/stock.csv') as csvfile:
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
def obtain_stock_from_variant (item_code, warehouse, quantity):
    # check_alternative_stock first
    alternate_stock = check_alternative_stock (item_code, warehouse)
    print (alternate_stock["qty"])
    if (float(alternate_stock["qty"]) < quantity ):
        frappe.throw (
            "Variant Quantity not sufficient for Stock Conversion"
        )
        return
    
    sles = get_stock_ledger_entries_for_item (item_code=item_code)
    
    for sle in sles:
        print (sle.as_dict())
    


    
    
    







# import csv
# with open('eggs.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))