# Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airplane(Document):
    def validate(self):
        self.check_duplicate_seats()
        self.check_capacity_equal_to_seats()

    def check_duplicate_seats(self):
        for seat in self.seats:
            count_seat = len(
                [s.seat for s in self.seats if seat.seat == s.seat]
            )
            if count_seat > 1:
                frappe.throw(f"Seat {seat.seat} already exists")

    def check_capacity_equal_to_seats(self):
        if self.capacity != len(self.seats):
            frappe.throw("Capacity must be equal to number of seats")
