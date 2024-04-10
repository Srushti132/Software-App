// Copyright (c) 2023, Srushti Gosai and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Software Expiry"] = {
	"filters": [
        // {
        //     "fieldname": "software_type",
        //     "label": "Software Type",
        //     "fieldtype": "Select",
		// 	"options": "--Select Software Type--\nOne Time PaidSubscription",
        //     "default": "--Select Software Type--"
        // },	
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
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "--Select Status--\nActive\nExpired"
        },	
	],

	"onload": function(report) {
		// report.set_filter_value("software_type", "");
		report.set_filter_value("start_date", "");
		report.set_filter_value("end_date", "");
        report.set_filter_value("status", "");

		report.refresh();
	}

    // "before_render": function(report) {
    //     var softwareTypeFilter = report.get_filter("software_type");
    //     var startDateFormatFilter = report.get_filter("start_date");
    //     var endDateFormatFilter = report.get_filter("end_date");    

    //     softwareTypeFilter.$input.on("change",function() {
    //         var selectedSoftwareType = softwareTypeFilter.get_value();

    //         if (selectedSoftwareType === "Free") {
    //             startDateFormatFilter.get_wrapper().hide();
    //             endDateFormatFilter.get_wrapper().hide();
    //         } else {
    //             startDateFormatFilter.get_wrapper().show();
    //             endDateFormatFilter.get_wrapper().show();
    //         }
    //     });
        // softwareTypeFilter.$input.trigger("change");
    // }
};