from datetime import datetime
from manager.parking_manager import ParkingManager
from strategy.fare_calculator import FareCalculator
from models.ticket import Ticket


class ParkingLot:
    def __init__(self, parking_manager: ParkingManager, fare_calculator: FareCalculator):
        self.parking_manager = parking_manager
        self.fare_calculator = fare_calculator
        self._active_tickets = {}   # license_plate → ticket

    def enter_vehicle(self, vehicle) -> Ticket:
        spot = self.parking_manager.find_spot_for_vehicle(vehicle)
        if spot is None:
            print(f"No available spot for {vehicle.get_license_plate()}.")
            return None
        self.parking_manager.park_vehicle(vehicle, spot)
        ticket = Ticket(vehicle, spot)
        self._active_tickets[vehicle.get_license_plate()] = ticket
        print(f"[ENTER] {vehicle.get_license_plate()} → spot {spot.get_spot_number()} ({spot.get_size().value})")
        return ticket

    def leave_vehicle(self, license_plate: str) -> float:
        ticket = self._active_tickets.get(license_plate)
        if ticket is None:
            print("No active ticket found.")
            return 0.0
        ticket.exit_time = datetime.now()
        fare = self.fare_calculator.calculate_fare(ticket)
        self.parking_manager.unpark_vehicle(ticket.vehicle, ticket.spot)
        del self._active_tickets[license_plate]
        print(f"[EXIT]  {license_plate} | duration: {ticket.calculate_parking_duration():.2f}h | fare: ${fare:.2f}")
        return fare
