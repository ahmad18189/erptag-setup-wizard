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
