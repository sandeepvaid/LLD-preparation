class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")

# Creating an instance of the Vehicle class
my_car = Vehicle("Toyota", "Camry", 2020)
# Calling the method to display information about the vehicle
my_car.display_info()