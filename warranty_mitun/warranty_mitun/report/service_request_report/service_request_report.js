frappe.query_reports["Service Request Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
        },
        {
            fieldname: "customer",
            label: "Customer",
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "warranty_status",
            label: "Warranty Status",
            fieldtype: "Select",
            options: "\nIn Warranty\nOut of Warranty"
        },
        {
            fieldname: "service_status",
            label: "Service Status",
            fieldtype: "Select",
            options: "\nDraft\nOpen\nIn Progress\nCompleted\nCancelled"
        }
    ]
};
