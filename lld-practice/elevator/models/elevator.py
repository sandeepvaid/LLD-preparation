from models.request import Request
from enums.direction import Direction
class Elevator:
    def __init__(self,elevator_id,current_floor = 0,total_floors = 10):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.total_floors = total_floors
        self.direction = Direction.IDLE
        self.requests = set()


    def step(self):
        #if not request is there
        if not self.requests:
            self.direction = Direction.IDLE
            return
        #Finding the nearest request and based on that set the elevator direction
        if self.direction == Direction.IDLE:
            min_distance = float('inf')
            nearest_request = None
            for request in self.requests:
                distance = abs(self.current_floor - request.requested_floor)
                if distance < min_distance:
                    min_distance = distance
                    nearest_request = request

            self.direction = Direction.UP if nearest_request.requested_floor > self.current_floor else Direction.DOWN

        #Now we check the floor right now elevator is the destination floor or not if yes then we remove the request from the set and if not then we move the elevator in the direction of the request
        pickup_request = Request(self.current_floor, self.direction)
        destination_request = Request(self.current_floor, Direction.IDLE)


        if pickup_request in self.requests or destination_request in self.requests:
            self.requests.discard(pickup_request)
            self.requests.discard(destination_request)
            if not self.requests:
                self.direction = Direction.IDLE
            return

        #if nothing remains ahead in the current direction, reverse (requests still exist behind us)
        if not self.any_request_ahead():
            if self.direction == Direction.UP:
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

    def any_request_ahead(self):
        for request in self.requests:
            if (self.direction == Direction.UP and request.requested_floor > self.current_floor) or (self.direction == Direction.DOWN and request.requested_floor < self.current_floor):
                return True
        return False

    def get_direction(self):
        return self.direction

    def get_current_floor(self):
        return self.current_floor

    def add_request(self,request):
        if request.requested_floor < 0 or request.requested_floor >= self.total_floors:
            print("Invalid floor request.")
            return False
        if self.current_floor == request.requested_floor:
            return True
        if request in self.requests:
            return True
        self.requests.add(request)
        return True

    def has_requests_at_or_beyond(self, floor, direction):
        for request in self.requests:
            if direction == Direction.UP and request.requested_floor >= floor:
                return True
            elif direction == Direction.DOWN and request.requested_floor <= floor:
                return True
        return False
        