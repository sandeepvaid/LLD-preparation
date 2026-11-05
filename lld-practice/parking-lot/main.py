from manager.parking_manager import ParkingManager
from strategy.base_fare_strategy import BaseFareStrategy
from strategy.peak_hours_fare_strategy import PeakHoursFareStrategy
from strategy.fare_calculator import FareCalculator
from models.compact_spot import CompactSpot
from models.regular_spot import RegularSpot
from models.oversized_spot import OversizedSpot
from models.motorcycle import Motorcycle
from models.car import Car
from models.truck import Truck
from parking_lot import ParkingLot


# --- Setup ---
manager = ParkingManager()
manager.add_spot(CompactSpot(101))
manager.add_spot(CompactSpot(102))
manager.add_spot(RegularSpot(201))
manager.add_spot(RegularSpot(202))
manager.add_spot(OversizedSpot(301))

# FareCalculator chains: base first, then peak multiplier
calculator = FareCalculator([BaseFareStrategy(), PeakHoursFareStrategy()])

lot = ParkingLot(manager, calculator)

# --- Simulation ---
print("=== Vehicles Entering ===")
lot.enter_vehicle(Motorcycle("MOTO-01"))
lot.enter_vehicle(Car("CAR-01"))
lot.enter_vehicle(Car("CAR-02"))
lot.enter_vehicle(Truck("TRUCK-01"))

print("\n=== No spot available (only 1 oversized spot) ===")
lot.enter_vehicle(Truck("TRUCK-02"))   # no oversized spot left

print("\n=== Vehicles Exiting ===")
lot.leave_vehicle("MOTO-01")
lot.leave_vehicle("CAR-01")
lot.leave_vehicle("TRUCK-01")
