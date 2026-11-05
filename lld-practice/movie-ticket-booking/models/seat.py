from ..enums.seat_type import SeatType

class Seat:
    def __init__(self, id: int, row: str, col: int, seatType: SeatType):
        self.id = id
        self.row = row
        self.col = col
        self.seatType = seatType