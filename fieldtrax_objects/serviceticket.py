class ServiceTicket:
    def __init__(self, id, job_id, description, status, 
                 assigned_to, due_date, priority, service_ticket_document=None):
        self.id = id
        self.job_id = job_id
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.due_date = due_date
        self.priority = priority
        self.notes = []
        self.service_ticket_document = service_ticket_document

    def add_note(self, note):
        self.notes.append(note)

    def update_status(self, new_status):
        self.status = new_status

    def get_status(self):
        return self.status