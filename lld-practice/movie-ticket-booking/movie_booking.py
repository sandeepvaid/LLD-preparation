from .concurrency.seat_locker import LockProvider
from .strategy.calculate_amount import RegularCalculateAmountStrategy
from .factory.payment_factory import PaymentFactory
from .enums.status import SeatStatus

class BookingService:
    def __init__(self):
        self.bookings = {}
        self.lock_provider = LockProvider()
        self.calculate_amount_strategy = RegularCalculateAmountStrategy()
        self.payment_strategy_factory = PaymentFactory()


    def create_booking(self,show,user,seat_ids,payment_method):
        try:
            self.lock_provider.lock_seat(seat_ids,user,show)
            amount = self.calculate_amount_strategy.calculate_amount(seat_ids,show.seat_price)
            if not self.payment_strategy_factory.get(payment_method).pay(amount):
                raise Exception(f"Payment failed for user {user} for show {show.id}")

            for seat_id in seat_ids:
                if self.lock_provider.validate_lock(seat_id,show,user):
                    show.show_seats[seat_id].status = SeatStatus.BOOKED
                    show.notify(f"Seat {seat_id} is booked by user {user} for show {show.id}")
                else:
                    raise Exception(f"Seat {seat_id} lock is not valid for user {user} for show {show.id}")
        finally:
            self.lock_provider.release_seat(seat_ids,user,show)

    def cancel_booking(self,show,user,seat_ids):
        for seat_id in seat_ids:
            if show.show_seats[seat_id].status == SeatStatus.BOOKED:
                show.show_seats[seat_id].status = SeatStatus.AVAILABLE
                show.notify(f"Seat {seat_id} is cancelled by user {user} for show {show.id}")