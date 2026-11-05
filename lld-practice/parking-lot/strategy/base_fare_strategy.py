from strategy.fare_strategy import FareStrategy
from enums.vehicle_size import VehicleSize


class BaseFareStrategy(FareStrategy):
    RATES = {
        VehicleSize.SMALL:  2.0,
        VehicleSize.MEDIUM: 3.0,
        VehicleSize.LARGE:  4.0,
    }

    def calculate_fare(self, ticket, current_fare: float) -> float:
        rate = self.RATES[ticket.vehicle.get_size()]
        return current_fare + rate * ticket.calculate_parking_duration()
