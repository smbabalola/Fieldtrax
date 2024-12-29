class DeliveryTicket:
    def __init__(self, ticket_number, job_id, date, item, quantity, unit, price, status):
        self.ticket_number = ticket_number
        self.job_id = job_id
        self.date = date
        self.item = item
        self.quantity = quantity
        self.unit = unit
        self.price = price
        self.status = status