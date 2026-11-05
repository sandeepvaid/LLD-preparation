from .show_seat import ShowSeat
from ..enums.status import SeatStatus

class Show:
    def __init__(self, id: int, seats, movie_id: int, theater_id: int, start_time: str, end_time: str):
        self.id = id
        self.show_seats = {seat.id:ShowSeat(seat) for seat in seats}
        self.movie_id = movie_id
        self.theater_id = theater_id
        self.start_time = start_time
        self.end_time = end_time
        self.observers = []

    def add_observer(self,obs):
        self.observers.append(obs)

    def notify(self,notification):
        for observer in self.observers:
            observer.update(notification)

    def get_available_show_seat(self):
        return [show_seat for show_seat in self.show_seats.values() if show_seat.status==SeatStatus.AVAILABLE]