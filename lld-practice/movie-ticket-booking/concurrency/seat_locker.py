from ..enums.status import SeatStatus
import threading

class SeatLock:
    def __init__(self, user, expiry):
        self.user, self.expiry = user, expiry

class SeatLocker:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        # double-checked locking so even the Singleton creation is thread-safe
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    inst = super().__new__(cls)
                    inst._mutex = threading.Lock()
                    inst._locks = {}
                    inst._clock = [0]
                    cls._instance = inst

    def _now(self):
        return self._clocks[0]

    def is_expired(self,lock):
        return self._now() > lock.expiry

    def lock_seat(self,seat_ids,user,show):
        with self._mutex:
            for seat_id in seat_ids:
                #check if any seat is already booked
                show_seat = show.show_seats[seat_id]
                if show_seat.status == SeatStatus.BOOKED:
                    raise Exception(f"Seat {seat_id} is already booked")

                #check if any seat is already locked
                existing_lock = self._locks.get((show.id,seat_id))
                # if existing_lock and 
                if (show.id,seat_id) in self._locks:
                    raise Exception(f"Seat {seat_id} is already locked by another user")

            for seat_id in seat_ids:
                self._locks[(show.id,seat_id)] = SeatLock(user,self._now() + 5)
                show.show_seats[seat_id].status = SeatStatus.LOCKED
                show.notify(f"Seat {seat_id} is locked by user {user} for show {show.id}")

    def release_seat(self,seat_ids,user,show):
        with self._mutex:
            for seat_id in seat_ids:
                existing_lock = self._locks.get((show.id,seat_id))
                if existing_lock and existing_lock.user == user:
                    del self._locks[(show.id,seat_id)]
                    show.show_seats[seat_id].status = SeatStatus.AVAILABLE
                    show.notify(f"Seat {seat_id} is released by user {user} for show {show.id}")

    def validte_lock(self,seat_id,show,user):
        existing_lock = self._locks.get((show.id,seat_id))
        if existing_lock and existing_lock.user == user and not self.is_expired(existing_lock):
            return True
        return False