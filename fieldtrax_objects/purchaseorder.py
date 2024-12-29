class PurchaseOrder:
    def __init__(self, id, jobid, vendor, date_created, due_date, terms, status):
        self.id = id
        self.vendor = vendor
        self.date_created = date_created
        self.due_date = due_date
        self.terms = terms
        self.status = status
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_total_amount(self):
        total = 0
        for item in self.items:
            total += item.quantity * item.price
        return total

class PurchaseOrderItem:
    def __init__(self, item_number, description, quantity, price):
        self.item_number = item_number
        self.description = description
        self.quantity = quantity
        self.price = price