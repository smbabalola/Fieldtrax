from datetime import datetime
class Tally:
    def __init__(self, id, job_id, date, time, activity, quantity):
        self.id = id
        self.job_id = job_id
        self.date = date
        self.time = time
        self.activity = activity
        self.quantity = quantity
        self.tally_items = []
        

class Tally_items:
    def __init__(self, id, item_number, description, joint_number, pipe_weight, pipe_length, accumulated_length,
                 depth, accumulated_weight, note):
        self.id = id
        self.item_number = item_number
        self.description = description
        self.joint_number = joint_number
        self.pipe_weight = pipe_weight
        self.pipe_length = pipe_length
        self.accumulated_length = accumulated_length
        self.depth = depth
        self.accumulated_weight = accumulated_weight
        self.note = note