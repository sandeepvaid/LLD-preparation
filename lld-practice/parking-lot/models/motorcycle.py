from models.vehicle import Vehicle
from enums.vehicle_size import VehicleSize


class Motorcycle(Vehicle):
    def get_size(self) -> VehicleSize:
        return VehicleSize.SMALL
