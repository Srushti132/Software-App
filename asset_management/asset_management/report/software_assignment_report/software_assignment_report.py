import frappe

def execute(filters):
    columns = [
        {
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Software Assignment",
            "label": "Software Assignment Id",
            "width": 200,
        },
        {
            "fieldname": "software_name",
            "fieldtype": "Data",
            "label": "Software Name",
            "width": 150,
        },
        {
            "fieldname": "purpose",
            "fieldtype": "Select",
            "label": "Purpose",
            "options": ["Assign","Re-Assign","Withdraw"],
            "width": 150,
        },
        {
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "label": "Transaction Date",
            "width": 150,
        },
    ]

    sql = """
        SELECT 
        DISTINCT SA.name, 
        SLI.software_name, 
        SA.purpose,
        SA.transaction_date,
        CASE
            WHEN SA.purpose IN ('Assign','Re-Assign') THEN SLI.to_employee
        END AS to_employee,
        CASE
            WHEN SA.purpose IN ('Withdraw','Re-Assign') THEN SLI.from_employee
        END AS from_employee
    
    FROM `tabSoftware Assignment` AS SA
    INNER JOIN `tabSoftware License Item` AS SLI 
    ON SLI.parent = SA.name
    WHERE 
        SA.docstatus > 0

    """
    
    if filters.get('purpose') != "Assign":
        columns.append(
            {
            "fieldname": "from_employee",
            "fieldtype": "Link",
            "options": "Employee",
            "label": "From Employee",
            "width": 150,
        },
        )
    
    if filters.get('purpose') != "Withdraw":
        columns.append(
            {
            "fieldname": "to_employee",
            "fieldtype": "Link",
            "options": "Employee",
            "label": "To Employee",
            "width": 150,
        },
        )


    if filters.get('purpose') == "Assign":
        sql += """
        AND (SA.purpose = 'Assign' AND SLI.to_employee IS NOT NULL)
        """
    elif filters.get('purpose') == "Withdraw":
        sql += """
        AND (SA.purpose = 'Withdraw' AND SLI.from_employee IS NOT NULL)
        """
    elif filters.get('purpose') == 'Re-Assign':
        sql += """
        AND (SA.purpose = 'Re-Assign' AND SLI.from_employee IS NOT NULL AND SLI.to_employee IS NOT NULL)
        """

    if filters.get('transaction_date1') and filters.get('transaction_date2'):
        sql+= """
            AND SA.transaction_date BETWEEN %(transaction_date1)s AND %(transaction_date2)s
        """
    data = frappe.db.sql(sql,filters,as_dict=1)

    for row in data:
        if row.get('to_employee'):
            row['to_employee'] = frappe.get_value("Employee", row['to_employee'], "employee_name")
        if row.get('from_employee'):
            row['from_employee'] = frappe.get_value("Employee", row['from_employee'], "employee_name")


    return columns, data