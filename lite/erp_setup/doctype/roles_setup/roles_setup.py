# -*- coding: utf-8 -*-
# Copyright (c) 2020, eng.ahmed-madi@hotmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.permissions import clear_user_permissions_for_doctype

class RolesSetup(Document):

    def on_update(self):
        self.setup_roles()

    def validate(self):
        if not self.accounts_manager:
            frappe.throw(_("Accounts Manager is mandatory"))

        if not self.hr_manager:
            frappe.throw(_("HR Manager is mandatory"))
        

        # self.remove_roles()

    def setup_roles(self):

       

        from frappe.utils.user import add_role
        for d in frappe.get_meta('Roles Setup').fields:
            if d.fieldtype == "Link" and d.options == "User":
                if self.get(d.fieldname):
                    add_role(self.get(d.fieldname), d.label)

                    if d.fieldname in ['hr_manager', 'hr_user', 'hr_viewer']:
                        clear_user_permissions_for_doctype("Employee", self.get(d.fieldname))

    # def remove_roles(self):
    #     for d in frappe.get_meta('Roles Setup').fields:
    #         if d.fieldtype == "Link" and d.options == "User":
    #             if self.get(d.fieldname):
    #                 user = frappe.get_doc("User", self.get(d.fieldname))
    #                 frappe.throw(self.get(d.fieldname))
    #                 user.remove_roles(d.label)

    #                 if d.fieldname in ['hr_manager', 'hr_user']:
    #                     emp = frappe.get_value("Employee", {"user_id": self.get(d.fieldname)}, "name")
    #                     if emp:
    #                         if not frappe.db.exists("User Permission", {"user": self.get(d.fieldname), "allow": "Employee", "for_value": emp}):
    #                             user_permission = frappe.new_doc("User Permission")
    #                             user_permission.user = self.get(d.fieldname)
    #                             user_permission.allow = "Employee"
    #                             user_permission.for_value = emp
    #                             user_permission.apply_to_all_doctypes = 1
    #                             user_permission.insert(ignore_permission = True)


                        # clear_user_permissions_for_doctype("Employee", self.get(d.fieldname))

