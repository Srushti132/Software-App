// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

function statusColorFormatter(value){
    var statusStyle = "";
    if (value == "Pending"){
        statusStyle = "color:red";
    }else if(value == "Ordered"){
        statusStyle = "color:green"
    }

    return `<span style = "${statusStyle}">${value}</span>`;
}

frappe.query_reports["Software Request"] = {


	"filters": [
        {
            "fieldname": "start_date",
            "label": "From Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "end_date",
            "label": "To Date",
            "fieldtype": "Date",
        },
		{
            "fieldname": "date_range",
            "label": __("Date Range"),
            "fieldtype": "Select",
            "options": "--Select Range--\nLast 2 Days\nLast Week\nLast 15 Days\nLast Month",
		},
        {
            "fieldname": "item_group",
            "label": "Type",
            "fieldtype": "Select",
			"options": "--Select Type--\nAsset\nSoftware License"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
			"options": "Draft\nSubmitted\nStopped\nCancelled\nPending\nPartially Ordered\nPartially Received\nOrdered\nIssued\nTransferred\nReceived",
            "default": " "
        },
	],
        "onload": function(report) {
            console.log("Onload event triggered");
            // Automatically clear filters when the report is refreshed
            report.set_filter_value("date_range", "");
            report.set_filter_value("start_date", "");
            report.set_filter_value("end_date", "");
            report.set_filter_value("item_group", "");
            report.set_filter_value("status", "");
            report.refresh();
        },
        
        "formatter": function (value, row, column, data, default_formatter) {
            value = default_formatter(value, row, column, data);

            // Check the column ID to target the "status" column
            if (column.id === "status") {
                if (value === "Pending") {
                    return "<span style='color: red !important;'>" + value + "</span>";
                } else if (value === "Ordered") {
                    return "<span style='color: green !important;'>" + value + "</span>";
                }
                // Add more conditions for other status values and formatting as needed
            }
    
            return value;
        }
}