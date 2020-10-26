# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
import json
# from dateutil import parser
# from datetime import date
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
    comma_or, get_fullname, add_years, add_months, add_days, nowdate , comma_and, get_datetime

from frappe.utils import cstr, nowdate, cint
from frappe import utils
from erpnext.setup.doctype.item_group.item_group import get_item_for_list_in_html
from erpnext.shopping_cart.product_info import set_product_info_for_website
import datetime
from datetime import date
from frappe.utils.password import update_password as _update_password
from frappe.utils.data import flt, nowdate, getdate, cint
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate , add_days
from pypaytabs import Paytabs
from pypaytabs import Utilities as util
import requests 





@frappe.whitelist(allow_guest=True)
def get_customer_logo_and_color():
    customer_color = '#190E2A'
    customer_logo = '/assets/mawred_theme/images/logo-white.png'
    doc = frappe.get_doc("System Setup")
    if doc.logo:
        customer_logo = doc.logo

    if doc.main_color:
        customer_color = doc.main_color

    return customer_logo, customer_color


@frappe.whitelist(allow_guest=True)
def edit_system_setup(logo, main_color, annual_leave_type, users_attach, no_items, items_attach, no_customers, customers_attach, no_suppliers, suppliers_attach, no_warehouses, warehouses_attach):
    doc = frappe.get_doc("System Setup")
    
    doc.main_color = main_color
    doc.annual_leave_type = annual_leave_type

    if len(logo)>7:
        doc.logo = logo
    else:
        doc.logo = ''

    if len(users_attach)>7:
        doc.employees_attachment = users_attach
    else:
        doc.employees_attachment = ''

    if len(items_attach)>7:
        doc.no_items = 0
        doc.items_attachment = items_attach
    else:
        doc.no_items = 1
        doc.items_attachment = ''

    if len(customers_attach)>7:
        doc.no_customers = 0
        doc.customers_attachment = customers_attach
    else:
        doc.no_customers = 1
        doc.customers_attachment = ''

    if len(suppliers_attach)>7:
        doc.no_suppliers = 0
        doc.suppliers_attachment = suppliers_attach
    else:
        doc.no_suppliers = 1
        doc.suppliers_attachment = ''

    if len(warehouses_attach)>7:
        doc.no_warehouses = 0
        doc.warehouses_attachment = warehouses_attach
    else:
        doc.no_warehouses = 1
        doc.warehouses_attachment = ''
    
    # doc.flags.ignore_mandatory = True
    # doc.save(ignore_permissions=True)
    
    doc.save()

    frappe.msgprint("Successfully saved!")

    return 1




@frappe.whitelist(allow_guest=True)
def get_system_setup_info():
    doc = frappe.get_doc("System Setup")
    return doc 




def create_viewer_roles():
	pass
def create_viewer_role(roles_parts):
	for part in roles_parts:
		if not frappe.db.exists("Role", {"role_name": part+" Viewer"}):
			doc = frappe.new_doc("Role")
			doc.role_name = part+" Viewer"
			doc.insert()
			print(part+" Viewer")
def update_roles_permissions():
	roles_first_parts = ["Accounts", "HR", "Stock", "Purchase", "Sales"]
	create_viewer_role(roles_first_parts)
	for rfp in roles_first_parts:
		manager_role = rfp+" Manager"
		user_role = rfp+" User"
		viewer_role = rfp+" Viewer"
		doctypes = frappe.db.sql_list("""select distinct(parent) from `tabDocPerm` where 
			role = '{0}' or role = '{1}' or role = '{2}'""".format(manager_role, user_role, viewer_role))
		for d in doctypes:
			insert_custom_docperm(d, [manager_role, user_role, viewer_role])

def insert_custom_docperm(d, roles, permlevel = 0):
	for role in roles:
		existed_cdp = frappe.db.exists('Custom DocPerm', dict(parent = d, role = role, permlevel = permlevel))
		meta = frappe.get_meta(d)
		perms = {
			"doctype":"Custom DocPerm",
			"parent": d,
			"parenttype": "DocType",
			"parentfield": "permissions",
			"role": role,
			'read': 1,
			'write': 1 if not "Viewer" in role else 0,
			'create': 1 if not "Viewer" in role else 0,
			'delete': 1 if not "Viewer" in role else 0,
			'print': 1 if not "Viewer" in role else 0,
			'report': 1 if not "Viewer" in role else 0,
			'export': 1 if not "Viewer" in role else 0,
			'submit': 1 if "Manager" in role and meta.is_submittable else 0,
			'cancel': 1 if "Manager" in role and meta.is_submittable else 0,
			'import': 0 if not cint(meta.allow_import) else 1,
			"permlevel": 0
		}
		if not existed_cdp:
			custom_docperm = frappe.get_doc(perms)
			custom_docperm.__islocal = 1
			custom_docperm.save()
		else:
			custom_docperm = frappe.get_doc("Custom DocPerm", existed_cdp)
			custom_docperm.update(perms)
			custom_docperm.save()
		print(d + " --- " + role)






def block_modules():
	modules = frappe.db.sql_list("select name from `tabModule Def`")
	modules += ["Getting Started", "Leaderboard", "dashboard", "Marketplace",
	 "Settings", "Users and Permissions", "Customization", "Learn", "Help"]
	# print(modules)
	for m in modules:
		if m == "ERP Setup":
			if frappe.db.exists("Block Module", {"module": m, "parent": "Administrator"}):
				frappe.db.sql("delete from `tabBlock Module` where module = '{0}'".format(m))
		else:
			if not frappe.db.exists("Block Module", {"module": m, "parent": "Administrator"}):
				doc = frappe.get_doc('User', 'Administrator')
				# doc.set('block_modules', [])
				doc.append('block_modules', {
					'module': m
				})


				doc.save(ignore_permissions=True)
	#add erp setup to show

def unblock_modules(module):

	# modules = ["Accounts", "HR", "Buying", "Selling", "Stock"]
	# erp_setup = frappe.get_single("System Setup")
	# for m in modules:
	# 	# m_name = frappe.get_value("Block Module", filters = {"module": m}, filedname = "name")
	# 	# frappe.delete_doc("Block", m_name, force=True)
	# 	if erp_setup.no_suppliers and m == "Buying":
	# 		continue
	# 	if erp_setup.no_customers and m == "Selling":
	# 		continue
	# 	if erp_setup.no_items and m == "Stock":
	# 		continue
	frappe.db.sql("delete from `tabBlock Module` where module = '{0}'".format(module))

	# doc = frappe.get_doc('User', 'Administrator')
	# doc.append('block_modules', {
	# 	'module': 'ERP Setup'
	# })
	users = frappe.get_all("User")
	for user in users:
		if user['name'] not in ['Administrator', 'Guest'] and 'System Manager' not in frappe.get_roles(user['name']):
			doc = frappe.get_doc('User', user['name'])
			doc.append('block_modules', {
				'module': 'ERP Setup'
			})
			frappe.flags.in_import = True
			doc.save(ignore_permissions=True)
