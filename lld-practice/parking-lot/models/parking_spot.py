from abc import ABC, abstractmethod
from enums.vehicle_size import VehicleSize


class ParkingSpot(ABC):
    def __init__(self, spot_number: int):
        self.spot_number = spot_number
        self._vehicle = None

    @abstractmethod
    def get_size(self) -> VehicleSize:
        pass

    def is_available(self) -> bool:
        return self._vehicle is None

    def occupy(self, vehicle):
        self._vehicle = vehicle

    def vacate(self):
        self._vehicle = None

    def get_spot_number(self) -> int:
        return self.spot_number
