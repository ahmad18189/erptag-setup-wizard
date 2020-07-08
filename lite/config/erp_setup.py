from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Setups"),
			"items": [
				{
					"type": "doctype",
					"name": "System Setup",
					"description": _("System Setup"),
					"label": _("System Setup"),
					"onboard": 1,
					"icon": "fa fa-star",
				},
				{
					"type": "doctype",
					"name": "Roles Setup",
					"description": _("Roles Setup"),
					"label": _("Roles Setup"),
					"onboard": 1,
					"icon": "fa fa-star",
				}

			]
		}
		
	]