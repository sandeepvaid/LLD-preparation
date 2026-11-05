from enums.direction import Direction
from models.request import Request
class ElevatorController:
    def __init__(self,elevators):
        self.elevators = elevators


    def request_elevator(self,requested_floor,direction):
        request = Request(requested_floor, direction)
        best = self.select_best_elevator(request)
        if best is None:
            return False

        return best.add_request(request)

    def select_best_elevator(self,request):

        best_elevator = self.find_committed_to_floor(request)
        if best_elevator is not None:
            return best_elevator
        best_elevator = self.find_idle_elevator(request)
        if best_elevator is not None:
            return best_elevator
        best_elevator = self.find_closest_elevator(request)
        return best_elevator

    def find_committed_to_floor(self,request):
        request_floor = request.get_floor()
        min_distance = float('inf')
        best_elevator = None
        for elevator in self.elevators:
            if elevator.get_direction() != request.get_direction():
                continue
            if (elevator.get_direction() == Direction.UP and elevator.get_current_floor() > request_floor) or (elevator.get_direction() == Direction.DOWN and elevator.get_current_floor() < request_floor):
                continue

            if not elevator.has_requests_at_or_beyond(request_floor, request.get_direction()):
                continue

            distance = abs(elevator.get_current_floor() - request_floor)
            if distance < min_distance:
                min_distance = distance
                best_elevator = elevator

        return best_elevator

    def find_idle_elevator(self,request):
        request_floor = request.get_floor()
        min_distance = float('inf')
        best_elevator = None
        for elevator in self.elevators:
            if elevator.get_direction() != Direction.IDLE:
                continue

            distance = abs(elevator.get_current_floor() - request_floor)
            if distance < min_distance:
                min_distance = distance
                best_elevator = elevator

        return best_elevator

    def find_closest_elevator(self,request):
        request_floor = request.get_floor()
        min_distance = float('inf')
        best_elevator = None
        for elevator in self.elevators:
            distance = abs(elevator.get_current_floor() - request_floor)
            if distance < min_distance:
                min_distance = distance
                best_elevator = elevator

        return best_elevator

    def step(self):
        for elevator in self.elevators:
            elevator.step()
