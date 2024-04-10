frappe.query_reports["Software Assignment Report"] = {
	"filters": [
		{
			'fieldname':'purpose',
			'label':'Purpose',
			'fieldtype':'Select',
			'options': [" ",'Assign','Re-Assign','Withdraw'],
			'default':" ",
			'width': 100
		},
		{
			"fieldname": "transaction_date1",
			"label": "To Date",
			"fieldtype": "Date",
			"default": null
		},
		{
			"fieldname": "transaction_date2",
			"label": "From Date",
			"fieldtype": "Date",
			"default": null
		},
	],
	onload: function(report) {
        report.set_filter_value('purpose', ' ');  
        report.set_filter_value('transaction_date1', null); 
        report.set_filter_value('transaction_date2', null); 
    },
};