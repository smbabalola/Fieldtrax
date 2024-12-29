class Personnel:
    def __init__(self, personnel_id, name, role, department, start_date, end_date=None):
        self.personnel_id = None
        self.name = name
        self.role = role
        self.department = department
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self):
        return self.end_date is None