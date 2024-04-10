# Copyright (c) 2023, Srushti Gosai and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import msgprint, _
from datetime import datetime, timedelta

def execute(filters=None):

	sql = """
			SELECT
				sl.software_id,
				# sl.software_type,
				sl.software_name,
				sl.software_category,
				sl.start_date,
				sl.end_date,
				GROUP_CONCAT(DISTINCT slu.user ORDER BY slu.user SEPARATOR ', ') AS user
			FROM
				`tabSoftware License` AS sl
			LEFT JOIN
				`tabSoftware License Users` AS slu
			ON
				slu.parent = sl.name
			WHERE
				sl.software_type = "Subscription"
			GROUP BY
				sl.software_id;
	"""

	# ,GROUP_CONCAT(slu.user SEPARATOR ', ') AS users

	conditions = []
	current_date = datetime.now().strftime('%Y-%m-%d')

	if filters:
		# software_type = filters.get("software_type")
		start_date = filters.get("start_date")
		end_date = filters.get("end_date")
		status = filters.get("status")

		# if software_type:
		# 	if software_type == 'One Time Paid':  # Use "elif" here
		# 		conditions.append(f"software_type = 'One Time Paid'")
		# 	elif software_type == 'Subscription':  # Use "elif" here
		# 		conditions.append(f"software_type = 'Subscription'")

		if start_date and end_date:
			conditions.append(f"end_date BETWEEN '{start_date}' AND '{end_date}'")
		
		if status:
			if status == "Active":
				conditions.append(f"end_date > '{current_date}'")
			if status == "Expired":
				conditions.append(f"end_date < '{current_date}'")

		if conditions:
			sql += " AND " + " AND ".join(conditions)


	columns = [
		{
			"fieldname": "software_id",
			"label" : "Software ID",
			"fieldtype" : "Link",
			"width": "160",
			"options": "Software License"
		},
		# {
		# 	"fieldname": "software_type",
		# 	"label" : "Software Type",
		# 	"fieldtype" : "Data",
		# 	"width": "160",
		# },
		{
			"fieldname": "software_name",
			"label" : "Software Name",
			"fieldtype" : "Data",
			"width": "160",
		},
		{
			"fieldname": "software_category",
			"label" : "Software Category",
			"fieldtype" : "Data",
			"width": "160",
		},
		{
			"fieldname": "start_date",
			"label" : "Start Date",
			"fieldtype" : "date",
			"width": "160",
		},
		{
			"fieldname": "end_date",
			"label" : "End Date",
			"fieldtype" : "date",
			"width": "160",
		},
		{
			"fieldname": "user",
			"label" : "User Name",
			"fieldtype" : "Link",
			"options": "Employee",
			"width": "160",
		},

	]

	if filters.get("software_type") == "Free":
		columns = [col for col in columns if col["fieldname"] not in  ["start_date","end_date"]]

	data = frappe.db.sql(sql, as_dict=True)
	return columns, data