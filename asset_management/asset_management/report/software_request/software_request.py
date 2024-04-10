# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from datetime import datetime, timedelta


def execute(filters=None):
	
    sql = """SELECT mre.name,
                mre.transaction_date,
                mre.schedule_date,
                mre.item_name,
                mre.item_group,
                mre.owner,
                mre.qty,
                mre.rate,
                mre.amount,
                mre.status,
                CASE
                    WHEN ti.item_group = 'Software License' THEN sl.software_category
                    ELSE ti.asset_category
                END as asset_category
            FROM   (
                            SELECT     mr.name,
                                        mr.owner,
                                        mr.status,
                                        mr.transaction_date,
                                        mr.schedule_date,
                                        mr.material_request_type,
                                        mri.item_name,
                                        mri.item_group,
                                        mri.qty,
                                        mri.rate,
                                        mri.amount
                            FROM       `tabMaterial Request`      AS mr
                            INNER JOIN `tabMaterial Request Item` AS mri
                            ON         mri.parent = mr.name ) AS mre
            JOIN   `tabItem`                                    AS ti
            ON     ti.item_name = mre.item_name
            LEFT JOIN `tabSoftware License` AS sl
            ON sl.software_name = mre.item_name
            WHERE (ti.item_group = 'Software License' OR ti.is_fixed_asset = 1)
            """
    conditions = []

    if filters:
        date_range = filters.get("date_range")
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        item_group = filters.get("item_group")
        status = filters.get("status")

        if item_group:
            if item_group == 'Software License':
                conditions.append(f"ti.item_group = 'Software License'")
            if item_group == 'Asset':
                conditions.append(f"ti.item_group != 'Software License'")

        
        if start_date and end_date:
            conditions.append(f"mre.transaction_date BETWEEN '{start_date}' AND '{end_date}'")
        
        if date_range:

            if date_range == "Last 2 Days":
                end_date = datetime.now()
                start_date = end_date - timedelta(days=2)
            elif date_range == "Last Week":
                end_date = datetime.now()
                start_date = end_date - timedelta(weeks=1)
            elif date_range == "Last 15 Days":
                end_date = datetime.now()
                start_date = end_date - timedelta(days=15)
            elif date_range == "Last Month":
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30) 

            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            conditions.append(f"mre.transaction_date BETWEEN '{start_date_str}' AND '{end_date_str}'")     

        if status:
            conditions.append(f"mre.status = '{status}'")

        if conditions:
            sql += " AND " + " AND ".join(conditions)
 
    data = frappe.db.sql(sql, as_dict=True)

    columns = [
        {
            "fieldname": "name",
            "label": "Material Request",
            "fieldtype": "Link",
            "width": "160",
            "options" : "Material Request"
        },
        {
            "fieldname": "item_name",
            "label": "Item",
            "fieldtype": "Data",
            "width": "130"
        },
        {
            "fieldname": "qty",
            "label": "Qty",
            "fieldtype": "Float",
            "width": "50"
        },
        {
            "fieldname": "rate",
            "label": "Rate",
            "fieldtype": "Float",
            "width": "90"
        },
        {
            "fieldname": "amount",
            "label": "Amount",
            "fieldtype": "Float",
            "width": "90"
        },
        {
            "fieldname": "transaction_date",
            "label": "Request Date",
            "fieldtype": "Date",
            "width": "100"
        },
        {
            "fieldname": "schedule_date",
            "label": "Required By",
            "fieldtype": "Date",
            "width": "100"
        },
        {
            "fieldname": "owner",
            "label": "Requested By",
            "fieldtype": "Data",
            "width": "130"
        },
        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Data",
            "width": "100"  
        },
                {
            "fieldname": "asset_category",
            "label": "Category",
            "fieldtype": "Data",
            "width": "100"  
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": "70" 
        }
    ]

    return columns, data