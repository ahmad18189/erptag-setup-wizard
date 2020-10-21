from __future__ import unicode_literals
import frappe
from frappe.desk.moduleview import get_data
# from frappe.config import get_modules_from_all_apps_for_user
from mawred_theme.get_modules import get_modules_from_all_apps_for_user
from frappe.utils import cint

def boot_session(bootinfo):
	"""boot session - send website info if guest"""
	if frappe.session['user']!='Guest':

		bootinfo.sidebar_modules = sidebar_modules()
		bootinfo.notifications = modules_notification()
		bootinfo.standard_modules_view = get_standard_modules_view()
		
def sidebar_modules():
	all_modules = get_modules_from_all_apps_for_user()
	allowed = [d for d in all_modules if (d["type"] == 'module' and not d.get('blocked') )]
	modules = {}
	for module in allowed:
		name = module['module_name']
		data = get_data(name)

		if len(data)> 0:
			modules[module['module_name']] = module 

	return modules

@frappe.whitelist(allow_guest=True)
def get_standard_modules_view():
	
	if not frappe.get_meta('User').has_field('standard_modules_view'):
		return 0
	
	standard_modules_view = frappe.db.get_value(
								"User",
								frappe.session.user,
								"standard_modules_view")
	return standard_modules_view

@frappe.whitelist(allow_guest=True)
def modules_notification():
	user = frappe.session.user
	read_field_exists = frappe.db.sql("""
		SHOW COLUMNS FROM `tabNotification Log` LIKE 'read'
	""")
	seen_field_exists = frappe.db.sql("""
		SHOW COLUMNS FROM `tabNotification Log` LIKE 'seen'
	""")
	read_status_field = "log.read"
	if seen_field_exists:
		read_status_field = "log.seen"

	notifications = frappe.db.sql("""  
		select count(log.name) count,doctype.module,doctype.name  
		from `tabNotification Log` as log  
		Left Join `tabDocType` as doctype On log.document_type = doctype.name  
		where log.for_user = '{user}' and {read_field} != 1  
		Group By doctype.module  
	""".format(user=user,read_field=read_status_field),as_dict=1)

	notifications_dict = dict()
	for notification in notifications:
		notifications_dict[notification["module"]] = [notification["count"]]

	return notifications_dict

	notifications_dict = dict()
	for notification in notifications:
		notifications_dict[notification["name"]] = [notification["count"]]

	return notifications_dict

@frappe.whitelist(allow_guest=True)
def get_doctype_value(doctype,docname,field):
	value = frappe.db.get_value(doctype,docname,field)
	return value
