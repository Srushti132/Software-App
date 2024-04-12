// Copyright (c) 2024, srushti and contributors
// For license information, please see license.txt

frappe.ui.form.on("Software Assets", {
  refresh(frm) {
    frm.set_query("hr_manager", function () {
      return {
        filters: [["designation", "=", "HR Manager"]],
      };
    });
  },
});
