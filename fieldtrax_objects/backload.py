class Backload:
    def __init__(self, id, job_id, well_name, rig_name, po_number, personnel, 
                 date_created, due_date, ship_to, contact_phone, status, signed_backload_sheet):
        self.id = id
        self.job_id = job_id
        self.wellname = well_name
        self.rigname = rig_name
        self.po_number = po_number
        self.personnel = []
        self.date_created = date_created
        self.due_date = due_date
        self.ship_to = ship_to
        self.contact_phoneno = contact_phone
        self.status = status
        self.items = []
        self.signed_backload_sheet = signed_backload_sheet

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

class BackloadItem:
    def __init__(self, item_number, serial_number, quantity, description, status, 
                 date_returned, condition, returned_to):
        self.item_number = item_number
        self.serial_number = serial_number
        self.quantity = quantity
        self.description = description
        self.status = status
        self.date_returned = date_returned
        self.condition = condition
        self.returned_to = returned_to