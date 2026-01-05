import frappe
from frappe.utils import add_months

def calculate_warranty_expiry(doc, method):
    print(f"\n[WARRANTY DEBUG] calculate_warranty_expiry called for {doc.name}")

    for item in doc.items:
        if not item.item_code:
            continue

        warranty_period = frappe.db.get_value(
            "Item",
            item.item_code,
            "custom_warranty_period"
        )

        print(f"[WARRANTY DEBUG] Retrieved warranty_period for {item.item_code}: {warranty_period}")

        if warranty_period:
            expiry_date = add_months(
                doc.posting_date,
                int(warranty_period)
            )

            # 🔴 DIRECT DB UPDATE (THIS IS THE KEY)
            frappe.db.set_value(
                "Sales Invoice Item",
                item.name,
                "custom_warranty_expiry_date",
                expiry_date
            )

            print(
                f"[WARRANTY DEBUG] Item: {item.item_code} | "
                f"Expiry Date STORED: {expiry_date}"
            )
