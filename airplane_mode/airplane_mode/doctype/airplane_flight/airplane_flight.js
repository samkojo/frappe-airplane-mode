// Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
    frm.add_custom_button( "Submit All Tickets",
      () => {
        frm.call('submit_all_airplane_tickets')
        // frappe.show_alert("Submit All Tickets");
      }
    )
	},
});
