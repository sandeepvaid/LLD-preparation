from enums.vehicle_size import VehicleSize


class ParkingManager:
    def __init__(self):
        self.available_spots = {
            VehicleSize.SMALL:  [],
            VehicleSize.MEDIUM: [],
            VehicleSize.LARGE:  [],
        }
        self._vehicle_to_spot = {}   # license_plate → spot
        self._spot_to_vehicle = {}   # spot_number → vehicle

    def add_spot(self, spot):
        self.available_spots[spot.get_size()].append(spot)

    def find_spot_for_vehicle(self, vehicle):
        spots = self.available_spots[vehicle.get_size()]
        return spots[0] if spots else None

    def park_vehicle(self, vehicle, spot):
        self.available_spots[spot.get_size()].remove(spot)
        spot.occupy(vehicle)
        self._vehicle_to_spot[vehicle.get_license_plate()] = spot
        self._spot_to_vehicle[spot.get_spot_number()] = vehicle

    def unpark_vehicle(self, vehicle, spot):
        spot.vacate()
        self.available_spots[spot.get_size()].append(spot)
        del self._vehicle_to_spot[vehicle.get_license_plate()]
        del self._spot_to_vehicle[spot.get_spot_number()]

    def find_spot_by_vehicle(self, license_plate):
        return self._vehicle_to_spot.get(license_plate)

    def find_vehicle_by_spot(self, spot_number):
        return self._spot_to_vehicle.get(spot_number)
