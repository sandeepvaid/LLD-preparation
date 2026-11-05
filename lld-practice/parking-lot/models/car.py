from models.vehicle import Vehicle
from enums.vehicle_size import VehicleSize


class Car(Vehicle):
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM
