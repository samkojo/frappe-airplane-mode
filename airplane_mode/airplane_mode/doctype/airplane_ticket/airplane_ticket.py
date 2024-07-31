# Copyright (c) 2024, fujimoto.samuel@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        # Generate random integer 2 digits and random letter from A to E
        import random
        random_number = random.randint(10, 99)
        random_letter = chr(random.randint(65, 69))
        self.seat = f"{random_number}{random_letter}"

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
