import frappe
from frappe.utils import today, date_diff, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Request Date",
            "fieldname": "request_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180
        },
        {
            "label": "Item",
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 120
        },
        {
            "label": "Warranty Expiry Date",
            "fieldname": "warranty_expiry_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": "Service Status",
            "fieldname": "service_status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Warranty Status",
            "fieldname": "warranty_status",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": "Days Until Expiry",
            "fieldname": "days_until_expiry",
            "fieldtype": "Int",
            "width": 140
        },
    ]


def get_data(filters):
    if not filters:
        filters = {}

    data = []

    service_requests = frappe.get_all(
        "Service Request",
        fields=["name", "request_date", "customer", "service_status"],
        filters={
            "docstatus": ["<", 2]
        }
    )

    for sr in service_requests:
        items = frappe.get_all(
            "Service Request Item",
            fields=["item_code", "warranty_expiry_date"],
            filters={"parent": sr.name}
        )

        for item in items:
            warranty_status = "Out of Warranty"
            days_until_expiry = 0

            if item.warranty_expiry_date:
                expiry_date = getdate(item.warranty_expiry_date)
                today_date = getdate(today())

                if expiry_date >= today_date:
                    warranty_status = "In Warranty"
                    days_until_expiry = date_diff(expiry_date, today_date)

            # Filter: Warranty Status
            if filters.get("warranty_status") and filters.get("warranty_status") != warranty_status:
                continue

            data.append({
                "request_date": sr.request_date,
                "customer": sr.customer,
                "item": item.item_code,
                "warranty_expiry_date": item.warranty_expiry_date,
                "service_status": sr.service_status,
                "warranty_status": warranty_status,
                "days_until_expiry": days_until_expiry
            })

    return data
