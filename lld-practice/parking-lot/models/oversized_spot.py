from models.parking_spot import ParkingSpot
from enums.vehicle_size import VehicleSize


class OversizedSpot(ParkingSpot):
    def get_size(self) -> VehicleSize:
        return VehicleSize.LARGE
