# Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
    def get_full_name(self):
        if not self.last_name:
            return f"{self.first_name}"
        return f"{self.first_name} {self.last_name}"

    def before_save(self):
        self.full_name = self.get_full_name()
