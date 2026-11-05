import uuid
from datetime import datetime


class Ticket:
    def __init__(self, vehicle, spot):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None

    def calculate_parking_duration(self) -> float:
        end = self.exit_time or datetime.now()
        hours = (end - self.entry_time).total_seconds() / 3600
        return max(hours, 1.0)   # minimum 1 hour billing
