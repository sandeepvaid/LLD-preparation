from ..enums.status import SeatStatus

class ShowSeat:
    def __init__(self, show_id: int, seat_id: int, is_booked: bool, status: str):
        self.show_id = show_id
        self.seat_id = seat_id
        self.status = SeatStatus.AVAILABLE
        self.is_booked = is_booked