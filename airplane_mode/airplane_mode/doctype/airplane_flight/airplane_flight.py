# Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
# For license information, please see license.txt

from frappe.website.website_generator import WebsiteGenerator
import frappe


class AirplaneFlight(WebsiteGenerator):
    # website = frappe._dict(
    #     template="templates/generators/job_opening.html",
    #     condition_field="published",
    #     page_title_field="job_title",
    # )

    def get_context(self, context):
        # show breadcrumbs
        context.parents = [
            {
                "name": "flights",
                "title": frappe._("All Flights"),
                "route": "/flights"
            }
        ]

    # def set_title(self):
    #     date_of_departure = datetime.strptime(
    #         self.date_of_departure, '%Y-%m-%d'
    #     )
    #     return '-'.join([
    #         date_of_departure.strftime('%Y%m%d'),
    #         self.source_airport_code,
    #         self.destination_airport_code,
    #         self.airplane,
    #     ])

    # def before_save(self):
    #     self.title = self.set_title()
    @frappe.whitelist()
    def submit_all_airplane_tickets(self):
        for ticket in frappe.get_all('Airplane Ticket', filters={'flight': self.name}):
            frappe.db.set_value('Airplane Ticket', ticket.name, 'docstatus', 1)
            frappe.db.commit()

        frappe.msgprint('All tickets submitted')

    def before_submit(self):
        self.status = "Completed"
