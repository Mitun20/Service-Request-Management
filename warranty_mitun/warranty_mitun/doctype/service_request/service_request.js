// Copyright (c) 2025, mitun and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Service Request", {
// 	refresh(frm) {

// 	},
// });
// console.log("Service Request JS Loaded");

frappe.ui.form.on("Service Request", {
    sales_invoice(frm) {
        if (!frm.doc.sales_invoice) return;

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Sales Invoice",
                name: frm.doc.sales_invoice
            },
            callback(r) {
                if (!r.message) return;

                const si = r.message;

                // Set customer
                frm.set_value("customer", si.customer);

                // Clear table
                frm.clear_table("service_request_items");

                (si.items || []).forEach(row => {
                    frm.add_child("service_request_items", {
                        item_code: row.item_code,
                        warranty_expiry_date: row.custom_warranty_expiry_date
                    });
                });

                frm.refresh_field("service_request_items");

                
            }
        });
    },

    refresh(frm) {
        frm.set_df_property("service_request_items", "cannot_add_rows", true);
        frm.set_df_property("service_request_items", "cannot_delete_rows", true);
    },

    validate(frm) {
        let today = frm.doc.request_date || frappe.datetime.get_today();
        let removed = [];

        frm.doc.service_request_items =
            frm.doc.service_request_items.filter(row => {
                if (row.warranty_expiry_date && row.warranty_expiry_date < today) {
                    removed.push(row.item_code);
                    return false;
                }
                return true;
            });

        if (removed.length) {
            frappe.msgprint({
                title: "Expired Warranty Items Removed",
                message: removed.join(", "),
                indicator: "orange"
            });
        }
    }
});
