from abc import ABC, abstractmethod
from enums.vehicle_size import VehicleSize


class Vehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

    @abstractmethod
    def get_size(self) -> VehicleSize:
        pass

    def get_license_plate(self) -> str:
        return self.license_plate
