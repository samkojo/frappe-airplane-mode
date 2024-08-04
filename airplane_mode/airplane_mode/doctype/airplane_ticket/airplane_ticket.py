# Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def validate(self):
        self.check_has_seat_available()

    def check_has_seat_available(self):
        seats_occupied = frappe.db.count('Airplane Ticket', {'flight': self.flight, 'name': ('!=', self.name)})
        total_seats = frappe.get_value('Airplane Flight', {'name': self.flight}, 'airplane.capacity')
        if seats_occupied >= total_seats:
            frappe.throw('Flight is full')

    def before_insert(self):
        self.set_seat()

    def set_seat(self):
        if self.seat:
            return

        seats_occupied = frappe.get_all('Airplane Ticket', filters={'flight': self.flight}, fields=['seat'])
        seats_occupied = [seat['seat'] for seat in seats_occupied]
        airplane = frappe.get_value('Airplane Flight', {'name': self.flight}, 'airplane')
        seats = frappe.get_doc('Airplane', airplane).seats

        for seat in seats:
            if seat.seat not in seats_occupied:
                self.seat = seat.seat
                break

    def before_save(self):
        # Remove duplicate add ons
        # Initialize an empty dictionary to store the sums
        sums = {}

        # Iterate over each dictionary in the list
        for index, add_on in enumerate(self.add_ons):
            item = add_on.item
            amount = add_on.amount

            # If the item is already in the sums dictionary, add to the existing amount
            if item in sums:
                sums[item]['amount'] += amount
            else:
                # Otherwise, add the item to the sums dictionary with the current amount
                sums[item] = {'amount': amount, 'index': index}

        result = []
        for item, value in sums.items():
            add = self.add_ons[value['index']]
            add.amount = value['amount']
            result.append(add)

        self.add_ons = result

        self.total_amount = sum(add.amount for add in self.add_ons) + self.flight_price

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw('Status must be Boarded')
