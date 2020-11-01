# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
import json
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
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content_from_uploaded_file, read_csv_content
from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file, read_xls_file_from_attached_file
from frappe.utils.password import update_password
from frappe.utils import getdate, now_datetime, nowdate, date_diff
from frappe.permissions import clear_user_permissions_for_doctype



@frappe.whitelist(allow_guest=True)
def setup_system():
    setup_employees_and_users()
    setup_items()
    setup_customers()
    setup_suppliers()
    setup_warehouses()


def setup_employees_and_users():
    system_doc = frappe.get_doc("System Setup")

    if system_doc.employees_attachment:
        file = frappe.get_doc("File", {"file_url": system_doc.employees_attachment})
        filename = file.get_full_path()

        company = frappe.db.get_single_value('Global Defaults', 'default_company')
        abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')

        with open(filename, "r", encoding = "utf8") as infile:
            if frappe.safe_encode(filename).lower().endswith("csv".encode('utf-8')):
                rows = read_csv_content(infile.read())
            elif frappe.safe_encode(filename).lower().endswith("xls".encode('utf-8')):
                content = file.get_content()
                rows = read_xls_file_from_attached_file(fcontent=content)
            elif frappe.safe_encode(filename).lower().endswith("xlsx".encode('utf-8')):
                content = file.get_content()
                rows = read_xlsx_file_from_attached_file(fcontent=content)
            else:
                frappe.throw(_("Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload"))

            delete_nongroup_departments()
            delete_employment_types()
            delete_genders()
            delete_designations()
            delete_leave_types()
            delete_salary_components()
            insert_salary_components()
            insert_leave_types(system_doc.annual_leave_type)
            insert_leave_policy()

            for index, row in enumerate(rows):
                if index != 0:
                    if not row[0]:
                        frappe.throw(_("Employee Number column is mandatory"))
                    if not row[1]:
                        frappe.throw(_("Password column is mandatory"))
                    if not row[2]:
                        frappe.throw(_("First Name column is mandatory"))

                    user_email = row[0]+'@'+company+'.com'
                    insert_user(user_email, row[2], row[1], last_name = row[3])
                        
                    if row[9]:
                        insert_department(company, abbr, row[9])
                    else:
                        frappe.throw(_("Department column is mandatory"))

                    if row[10]:
                        insert_designation(row[10])
                    else:
                        frappe.throw(_("Designation column is mandatory"))
                    if row[10]:
                        insert_employment_type(row[8])
                    if row[4]:
                        insert_gender(row[4])
                    if not row[4]:
                        frappe.throw(_("Gender column is mandatory"))
                    if not row[6]:
                        frappe.throw(_("Date of Birth column is mandatory"))
                    if not row[7]:
                        frappe.throw(_("Date of Joining column is mandatory"))

                    set_employee_as_employee_number()
                    if not frappe.db.exists("Employee", row[0]):
                        doc = frappe.new_doc("Employee")
                        doc.employee_number = row[0]
                        doc.first_name = row[2]
                        doc.last_name = row[3]
                        doc.company = company 
                        doc.gender = row[4]
                        doc.country = row[5]
                        doc.date_of_birth = row[6]
                        doc.date_of_joining = row[7]
                        doc.employment_type = row[8]
                        doc.department = row[9] +' - '+abbr
                        doc.designation = row[10]
                        doc.cell_number = row[11]
                        doc.user_id = row[0]+'@'+company+'.com'
                        doc.leave_policy = frappe.db.sql("select name from `tabLeave Policy` order by creation desc limit 1")[0][0]
                        doc.insert(ignore_permissions=True)
                        frappe.db.commit()
                    allocate_leaves(system_doc.annual_leave_type, row[0], row[18])
                    if not row[12]:
                        frappe.throw(_("Basic Salary column is mandatory"))
                    else:
                        basic = row[12]
                    doj = row[7]
                    transportation = row[13]
                    housing = row[14]
                    mobile = row[15]
                    others = row[16]
                    gosi = row[17]
                    if not transportation:
                        transportation = 0
                    if not housing:
                        housing = 0
                    if not mobile:
                        mobile = 0
                    if not others:
                        others = 0
                    if not gosi:
                        gosi = "No"
                    insert_allowances(
                                row[0], 
                                basic,
                                doj, 
                                transportation, 
                                housing, 
                                mobile, 
                                others,
                                gosi
                                )


def insert_department(company, abbr, department):
    if not frappe.db.exists("Department", department+' - '+abbr):
        doc = frappe.new_doc("Department")
        doc.department_name = department
        doc.company = company
        doc.is_group = 0
        doc.insert(ignore_permissions=True)
        print(department)
        frappe.db.commit()

def delete_nongroup_departments():
    frappe.db.sql("delete from `tabDepartment` where is_group = 0")
    frappe.db.commit()

def delete_employment_types():
    frappe.db.sql("delete from `tabEmployment Type`")
    frappe.db.commit()

def delete_genders():
    frappe.db.sql("delete from `tabGender`")
    frappe.db.commit()

def delete_designations():
    frappe.db.sql("delete from `tabDesignation`")
    frappe.db.commit()

def delete_leave_types():
    frappe.db.sql("delete from `tabLeave Type`")
    frappe.db.commit()

def delete_salary_components():
    frappe.db.sql("delete from `tabSalary Component`")
    frappe.db.commit()

def insert_salary_components():
    if not frappe.db.exists("Salary Component", "Basic"):
        b_doc = frappe.new_doc("Salary Component")
        b_doc.salary_component = "Basic"
        b_doc.salary_component_abbr = "B"
        b_doc.is_payable = 1
        b_doc.depends_on_payment_days = 1
        b_doc.is_tax_applicable = 0
        b_doc.type = "Earning"
        b_doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Salary Component", "Transportation"):
        t_doc = frappe.new_doc("Salary Component")
        t_doc.salary_component = "Transportation"
        t_doc.salary_component_abbr = "T"
        t_doc.is_payable = 1
        t_doc.depends_on_payment_days = 1
        t_doc.is_tax_applicable = 0
        t_doc.type = "Earning"
        t_doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Salary Component", "Housing"):
        h_doc = frappe.new_doc("Salary Component")
        h_doc.salary_component = "Housing"
        h_doc.salary_component_abbr = "H"
        h_doc.is_payable = 1
        h_doc.depends_on_payment_days = 1
        h_doc.is_tax_applicable = 0
        h_doc.type = "Earning"
        h_doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Salary Component", "Mobile"):
        m_doc = frappe.new_doc("Salary Component")
        m_doc.salary_component = "Mobile"
        m_doc.salary_component_abbr = "M"
        m_doc.is_payable = 1
        m_doc.depends_on_payment_days = 1
        m_doc.is_tax_applicable = 0
        m_doc.type = "Earning"
        m_doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Salary Component", "Others"):
        m_doc = frappe.new_doc("Salary Component")
        m_doc.salary_component = "Others"
        m_doc.salary_component_abbr = "O"
        m_doc.is_payable = 1
        m_doc.depends_on_payment_days = 1
        m_doc.is_tax_applicable = 0
        m_doc.type = "Earning"
        m_doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Salary Component", "GOSI"):
        g_doc = frappe.new_doc("Salary Component")
        g_doc.salary_component = "GOSI"
        g_doc.salary_component_abbr = "GOSI"
        g_doc.is_payable = 1
        g_doc.depends_on_payment_days = 1
        g_doc.is_tax_applicable = 0
        g_doc.type = "Deduction"
        g_doc.insert(ignore_permissions = True)

    frappe.db.commit()


def insert_leave_types(annual_leave_type):
    if not frappe.db.exists("Leave Type", "Annual Leave-اجازة سنوية"):
        a_doc = frappe.new_doc("Leave Type")
        a_doc.leave_type_name = "Annual Leave-اجازة سنوية"
        a_doc.is_carry_forward = 1
        a_doc.max_leaves_allowed = 21 if annual_leave_type == "21 Days Without Holidays" else 30
        a_doc.include_holiday = 0 if annual_leave_type == "21 Days Without Holidays" else 1
        a_doc.save(ignore_permissions = True)

    if not frappe.db.exists("Leave Type", "Sick Leave-اجازة مرضية"):
        s_doc = frappe.new_doc("Leave Type")
        s_doc.leave_type_name = "Sick Leave-اجازة مرضية"
        a_doc.max_leaves_allowed = 30
        s_doc.include_holiday = 1
        s_doc.save(ignore_permissions = True)

    if not frappe.db.exists("Leave Type", "Leave Without Pay-اجازة بدون راتب"):
        w_doc = frappe.new_doc("Leave Type")
        w_doc.leave_type_name = "Leave Without Pay-اجازة بدون راتب"
        w_doc.is_lwp = 1
        w_doc.include_holiday = 1
        w_doc.save(ignore_permissions = True)
    frappe.db.commit()

def insert_leave_policy():
    lp = frappe.db.sql("select name from `tabLeave Policy` order by creation desc limit 1")
    if not lp:
        lp_doc = frappe.new_doc("Leave Policy")
        lp_doc.append("leave_policy_details", 
            {
                "leave_type": "Annual Leave-اجازة سنوية",
                "annual_allocation": 0
            }
        )
        lp_doc.append("leave_policy_details", 
            {
                "leave_type": "Sick Leave-اجازة مرضية",
                "annual_allocation": 0
            }
        )
        lp_doc.append("leave_policy_details", 
            {
                "leave_type": "Leave Without Pay-اجازة بدون راتب",
                "annual_allocation": 0
            }
        )
        lp_doc.save(ignore_permissions=True)
        lp_doc.submit()
        frappe.db.commit()


def insert_allowances(
    employee, 
    basic,
    doj, 
    transportation = 0, 
    housing = 0, 
    mobile = 0, 
    others = 0,
    gosi = "No"
    ):
    if not frappe.db.exists("Salary Structure", employee):
        ss_doc = frappe.new_doc("Salary Structure")
        ss_doc.name = employee
        # comps = ["Basic", "Transportation", "Housing", "Mobile", "Others", "GOSI"]
        # for comp in comps:

        ss_doc.append("earnings",{
            "salary_component": "Basic",
            "amount_based_on_formula": 1,
            "formula": "base"
        })
        ss_doc.append("earnings",{
            "salary_component": "Transportation",
            "amount_based_on_formula": 0,
            "amount": float(transportation)
        })
        ss_doc.append("earnings",{
            "salary_component": "Housing",
            "amount_based_on_formula": 0,
            "amount": float(housing)
        })
        ss_doc.append("earnings",{
            "salary_component": "Mobile",
            "amount_based_on_formula": 0,
            "amount": float(mobile)
        })
        ss_doc.append("earnings",{
            "salary_component": "Others",
            "amount_based_on_formula": 0,
            "amount": float(others)
        })
        if gosi.lower() == "yes":
            ss_doc.append("deductions",{
                "salary_component": "GOSI",
                "amount_based_on_formula": 1,
                "condition": "(base+H)<=45000",
                "formula": "(base+H)*0.1"
            })
            ss_doc.append("deductions",{
                "salary_component": "GOSI",
                "amount_based_on_formula": 1,
                "condition": "(base+H)>45000",
                "formula": "4500"
            })
        ss_doc.insert(ignore_permissions = True)
        ss_doc.submit()
        frappe.db.commit()
        if not frappe.db.exists("Salary Structure Assignment", {"employee": employee}):
            ssa_doc = frappe.new_doc("Salary Structure Assignment")
            ssa_doc.employee = employee
            ssa_doc.salary_structure = employee
            ssa_doc.from_date = doj
            ssa_doc.base = float(basic)
            ssa_doc.insert(ignore_permissions = True)
            ssa_doc.submit()



def allocate_leaves(annual_leave_type, employee, no_of_days):
    leave_types=["Annual Leave-اجازة سنوية","Sick Leave-اجازة مرضية"]
    employee_doc = frappe.get_doc("Employee", employee)
    current_year = str(getdate(nowdate()).year)
    for lt in leave_types:
        if not frappe.db.exists("Leave Allocation", {"employee": employee, "leave_type": lt}): 
            if lt == "Annual Leave-اجازة سنوية":
                if annual_leave_type == "21 Days Without Holidays":
                    nod = (21/365) * (date_diff(str(current_year)+"-12-31", nowdate()))
                else:
                    nod = (30/365) * (date_diff(str(current_year)+"-12-31", nowdate()))
                nod += float(no_of_days)
            elif lt == "Sick Leave-اجازة مرضية":
                nod = 100
            # else:
            #     nod = 200
            from_date = getdate(employee_doc.date_of_joining) if getdate(employee_doc.date_of_joining) > getdate(current_year+"-01-01") else current_year+"-01-01"
            la = frappe.new_doc('Leave Allocation')
            la.set("__islocal", 1)
            la.employee = employee
            la.employee_name = employee_doc.employee_name
            la.leave_type = lt
            la.from_date = from_date
            la.to_date = current_year+"-12-31"
            la.carry_forward = 1 if lt == "Annual Leave-اجازة سنوية" else 0
            la.new_leaves_allocated = round(nod)
            la.docstatus = 1
            la.save(ignore_permissions=True)
    frappe.db.commit()


def insert_designation(designation):
    if not frappe.db.exists("Designation", designation):
        doc = frappe.new_doc("Designation")
        doc.designation_name = designation
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

def insert_employment_type(employment_type):
    if not frappe.db.exists("Employment Type", employment_type):
        doc = frappe.new_doc("Employment Type")
        doc.employee_type_name = employment_type
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

def insert_gender(gender):
    if not frappe.db.exists("Gender", gender):
        doc = frappe.new_doc("Gender")
        doc.gender = gender
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

def insert_user(email, first_name, passowrd, last_name = None):
    if not frappe.db.exists("User", email):
        doc = frappe.new_doc("User")
        doc.email = email
        doc.first_name = first_name
        doc.last_name = last_name
        doc.send_welcome_email = 0
        frappe.flags.in_import = True
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        update_password(user=email, pwd=passowrd)

def set_employee_as_employee_number():
    hr_settings = frappe.get_single("HR Settings")
    hr_settings.emp_created_by = "Employee Number"
    hr_settings.save(ignore_permissions=True)
    frappe.db.commit()


def setup_roles(self):

    if not self.accounts_manager:
        frappe.throw(_("Accounts Manager is mandatory"))
    if not self.accounts_user:
        frappe.throw(_("Accounts User is mandatory"))
    if not self.hr_manager:
        frappe.throw(_("HR Manager is mandatory"))
    if not self.hr_user:
        frappe.throw(_("HR user is mandatory"))

    from frappe.utils.user import add_role
    for d in frappe.get_meta('System Setup').fields:
        if d.fieldtype == "Link" and d.options == "User":
            if self.get(d.fieldname):
                add_role(self.get(d.fieldname), d.label)

                if d.fieldname in ['hr_manager', 'hr_user']:
                    clear_user_permissions_for_doctype("Employee", self.get(d.fieldname))


def delete_nongroup_item_groups():
    item_groups = frappe.db.sql("select name from `tabItem Group` where is_group = 0", as_dict = True)
    for i in item_groups:
        frappe.delete_doc("Item Group", i['name'], force=True)
    frappe.db.commit()


def insert_items_group(company, item_group):
    if not frappe.db.exists("Item Group", item_group):
        doc =  frappe.new_doc("Item Group")
        doc.item_group_name = item_group
        items_group_parent = frappe.db.sql("select name from `tabItem Group` where is_group = 1 order by creation asc limit 1")[0][0] 
        doc.parent_item_group = items_group_parent
        expense_account = frappe.get_value("Company", company,"default_expense_account")
        if not expense_account:
            frappe.throw(_("Please insert the default expense account in Company"))

        income_account = frappe.get_value("Company", company,"default_income_account")
        if not income_account:
            frappe.throw(_("Please insert the default income account in Company"))

        doc.item_group_defaults = []
        doc.append("item_group_defaults", {

        "company": company,
        "expense_account": expense_account,
        "income_account": income_account

        })
        doc.is_group = 0
        doc.insert()
        frappe.db.commit()


def setup_items():
    system_doc = frappe.get_doc("System Setup")

    company = frappe.db.get_single_value('Global Defaults', 'default_company')
    abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')
    if system_doc.no_items:
        delete_nongroup_item_groups()
        #delete items also
        insert_items_group(company, "General Group")
        if not frappe.db.exists("Item", {"item_code": "General Stock"}):
                        
            i_doc = frappe.new_doc("Item")
            i_doc.item_code = "General Stock"
            i_doc.description = "General Stock"
            i_doc.is_stock_item = 1
            i_doc.include_item_in_manufacturing = 0
            i_doc.item_group = "General Group"
            i_doc.insert()
        if not frappe.db.exists("Item", {"item_code": "General Service"}):
                        
            i_doc = frappe.new_doc("Item")
            i_doc.item_code = "General Service"
            i_doc.description = "General Service"
            i_doc.is_stock_item = 0
            i_doc.include_item_in_manufacturing = 0
            i_doc.item_group = "General Group"
            i_doc.insert()

    elif system_doc.items_attachment:
        file = frappe.get_doc("File", {"file_url": system_doc.items_attachment})
        filename = file.get_full_path()

        with open(filename, "r", encoding = "utf8") as infile:
            if frappe.safe_encode(filename).lower().endswith("csv".encode('utf-8')):
                rows = read_csv_content(infile.read())
            elif frappe.safe_encode(filename).lower().endswith("xls".encode('utf-8')):
                content = file.get_content()
                rows = read_xls_file_from_attached_file(fcontent=content)
            elif frappe.safe_encode(filename).lower().endswith("xlsx".encode('utf-8')):
                content = file.get_content()
                rows = read_xlsx_file_from_attached_file(fcontent=content)
            else:
                frappe.throw(_("Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload"))

            delete_nongroup_item_groups()

            for index, row in enumerate(rows):
                if index != 0:
                    insert_items_group(company, row[3])
                    if not frappe.db.exists("Item", {"item_code": row[0]}):
                        
                        i_doc = frappe.new_doc("Item")
                        i_doc.item_code = row[0]
                        i_doc.description = row[1]
                        if row[2].lower() == "service":
                            i_doc.is_stock_item = 0
                        elif row[2].lower() == "stock":
                            i_doc.is_stock_item = 1
                        else:
                            frappe.throw(_("Item Type must be Service or Stock"))

                        i_doc.include_item_in_manufacturing = 0
                        i_doc.item_group = row[3]
                        i_doc.insert()


def setup_customers():
    system_doc = frappe.get_doc("System Setup")

    company = frappe.db.get_single_value('Global Defaults', 'default_company')
    abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')

    if system_doc.no_customers:
        delete_nongroup_customer_groups()
        delete_nongroup_territories()
        insert_customers_group(company, "General Group")
        insert_territories("General Territory")
        if not frappe.db.exists("Customer", "General Customer"):
            
            doc = frappe.new_doc("Customer")
            doc.customer_name = "General Customer"
            doc.customer_group = "General Group"
            doc.territory = "General Territory"
            doc.insert()

    elif system_doc.customers_attachment:
        file = frappe.get_doc("File", {"file_url": system_doc.customers_attachment})
        filename = file.get_full_path()

        with open(filename, "r", encoding = "utf8") as infile:
            if frappe.safe_encode(filename).lower().endswith("csv".encode('utf-8')):
                rows = read_csv_content(infile.read())
            elif frappe.safe_encode(filename).lower().endswith("xls".encode('utf-8')):
                content = file.get_content()
                rows = read_xls_file_from_attached_file(fcontent=content)
            elif frappe.safe_encode(filename).lower().endswith("xlsx".encode('utf-8')):
                content = file.get_content()
                rows = read_xlsx_file_from_attached_file(fcontent=content)
            else:
                frappe.throw(_("Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload"))

            delete_nongroup_customer_groups()
            delete_nongroup_territories()

            for index, row in enumerate(rows):
                if index != 0:
                    insert_customers_group(company, row[1])
                    insert_territories(row[2])
                    if not frappe.db.exists("Customer", row[0]):
                        
                        doc = frappe.new_doc("Customer")
                        doc.customer_name = row[0]
                        doc.customer_group = row[1]
                        doc.territory = row[2]
                        doc.insert()



def insert_customers_group(company, customer_group):
    if not frappe.db.exists("Customer Group", customer_group):
        doc =  frappe.new_doc("Customer Group")
        doc.customer_group_name = customer_group
        customers_group_parent = frappe.db.sql("select name from `tabCustomer Group` where is_group = 1 order by creation asc limit 1")[0][0] 
        doc.parent_customer_group = customers_group_parent
        account = frappe.get_value("Company", company,"default_receivable_account")
        if not account:
            frappe.throw(_("Please insert the default receivable account in Company"))

        doc.accounts = []
        doc.append("accounts", {

        "company": company,
        "account": account

        })
        doc.is_group = 0
        doc.insert()
        frappe.db.commit()

def delete_nongroup_customer_groups():
    customer_groups = frappe.db.sql("select name from `tabCustomer Group` where is_group = 0", as_dict = True)
    for i in customer_groups:
        frappe.delete_doc("Customer Group", i['name'], force=True)
    frappe.db.commit()

def insert_territories(territory):
    if not frappe.db.exists("Territory", territory):
        doc =  frappe.new_doc("Territory")
        doc.territory_name = territory
        territories_parent = frappe.db.sql("select name from `tabTerritory` where is_group = 1 order by creation asc limit 1")[0][0] 
        doc.parent_territory = territories_parent
        doc.is_group = 0
        doc.insert()
        frappe.db.commit()

def delete_nongroup_territories():
    territories = frappe.db.sql("select name from `tabTerritory` where is_group = 0", as_dict = True)
    for i in territories:
        frappe.delete_doc("Territory", i['name'], force=True)
    frappe.db.commit()


def setup_suppliers():
    system_doc = frappe.get_doc("System Setup")

    company = frappe.db.get_single_value('Global Defaults', 'default_company')
    abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')
    if system_doc.no_suppliers:
        delete_nongroup_supplier_groups()
        insert_suppliers_group(company, "General Group")
        if not frappe.db.exists("Supplier", "General Supplier"):
            doc = frappe.new_doc("Supplier")
            doc.supplier_name = "General Supplier"
            doc.supplier_group = "General Group"
            doc.supplier_type = "Individual"
            doc.insert()

    elif system_doc.suppliers_attachment:
        file = frappe.get_doc("File", {"file_url": system_doc.suppliers_attachment})
        filename = file.get_full_path()

        with open(filename, "r", encoding = "utf8") as infile:
            if frappe.safe_encode(filename).lower().endswith("csv".encode('utf-8')):
                rows = read_csv_content(infile.read())
            elif frappe.safe_encode(filename).lower().endswith("xls".encode('utf-8')):
                content = file.get_content()
                rows = read_xls_file_from_attached_file(fcontent=content)
            elif frappe.safe_encode(filename).lower().endswith("xlsx".encode('utf-8')):
                content = file.get_content()
                rows = read_xlsx_file_from_attached_file(fcontent=content)
            else:
                frappe.throw(_("Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload"))

            delete_nongroup_supplier_groups()

            for index, row in enumerate(rows):
                if index != 0:
                    insert_suppliers_group(company, row[1])
                    if not frappe.db.exists("Supplier", row[0]):
                        
                        doc = frappe.new_doc("Supplier")
                        doc.supplier_name = row[0]
                        doc.supplier_group = row[1]
                        if row[2].lower() == "individual":
                            doc.supplier_type = "Individual"
                        elif row[20].lower() == "company":
                            doc.supplier_type = "Company"
                        else:
                            frappe.throw(_("Supplier Type column values must be Company or Individual"))
                        doc.insert()


def insert_suppliers_group(company, supplier_group):
    if not frappe.db.exists("Supplier Group", supplier_group):
        doc =  frappe.new_doc("Supplier Group")
        doc.supplier_group_name = supplier_group
        suppliers_group_parent = frappe.db.sql("select name from `tabSupplier Group` where is_group = 1 order by creation asc limit 1")[0][0] 
        doc.parent_supplier_group = suppliers_group_parent
        account = frappe.get_value("Company", company,"default_payable_account")
        if not account:
            frappe.throw(_("Please insert the default payable account in Company"))

        doc.accounts = []
        doc.append("accounts", {

        "company": company,
        "account": account

        })
        doc.is_group = 0
        doc.insert()
        frappe.db.commit()

def delete_nongroup_supplier_groups():
    supplier_groups = frappe.db.sql("select name from `tabSupplier Group` where is_group = 0", as_dict = True)
    for i in supplier_groups:
        frappe.delete_doc("Supplier Group", i['name'], force=True)
    frappe.db.commit()

def setup_warehouses():
    system_doc = frappe.get_doc("System Setup")

    company = frappe.db.get_single_value('Global Defaults', 'default_company')
    abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')

    if system_doc.no_warehouses:
        delete_nongroup_warehouse_groups()
        if not frappe.db.exists("Warehouse", 'General Warehouse - '+abbr):
                        
            doc = frappe.new_doc("Warehouse")
            doc.warehouse_name = 'General Warehouse'
            doc.parent_warehouse = frappe.db.sql("select name from `tabWarehouse` where is_group = 1 order by creation asc limit 1")[0][0] 
            doc.insert()

    elif system_doc.warehouses_attachment:
        file = frappe.get_doc("File", {"file_url": system_doc.warehouses_attachment})
        filename = file.get_full_path()

        company = frappe.db.get_single_value('Global Defaults', 'default_company')
        abbr = frappe.get_value("Company", filters = {'name': company}, fieldname = 'abbr')

        with open(filename, "r", encoding = "utf8") as infile:
            if frappe.safe_encode(filename).lower().endswith("csv".encode('utf-8')):
                rows = read_csv_content(infile.read())
            elif frappe.safe_encode(filename).lower().endswith("xls".encode('utf-8')):
                content = file.get_content()
                rows = read_xls_file_from_attached_file(fcontent=content)
            elif frappe.safe_encode(filename).lower().endswith("xlsx".encode('utf-8')):
                content = file.get_content()
                rows = read_xlsx_file_from_attached_file(fcontent=content)
            else:
                frappe.throw(_("Only CSV and Excel files can be used to for importing data. Please check the file format you are trying to upload"))

            delete_nongroup_warehouse_groups()

            for index, row in enumerate(rows):
                if index != 0:
                    if not frappe.db.exists("Warehouse", row[0]+' - '+abbr):
                        
                        doc = frappe.new_doc("Warehouse")
                        doc.warehouse_name = row[0]
                        doc.parent_warehouse = frappe.db.sql("select name from `tabWarehouse` where is_group = 1 order by creation asc limit 1")[0][0] 
                        doc.insert()


def delete_nongroup_warehouse_groups():
    warehouses = frappe.db.sql("select name from `tabWarehouse` where is_group = 0", as_dict = True)
    for i in warehouses:
        frappe.delete_doc("Warehouse", i['name'], force=True)
    frappe.db.commit()









