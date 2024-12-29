from datetime import datetime
class TimesheetEntry:
    def __init__(self, date, start_time, end_time, activity, notes):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.notes = notes

class Timesheet:
    def __init__(self, job_id, employee_id, week_ending):
        self.job_id = job_id
        self.employee_id = employee_id
        self.week_ending = week_ending
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def calculate_total_hours(self):
        total_hours = 0
        for entry in self.entries:
            start_datetime = datetime.combine(entry.date, entry.start_time)
            end_datetime = datetime.combine(entry.date, entry.end_time)
            duration = end_datetime - start_datetime
            total_hours += duration.total_seconds() / 3600
        return total_hours