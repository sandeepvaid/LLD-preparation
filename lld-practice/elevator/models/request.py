class Request:
    def __init__(self, requested_floor, direction):
        self.requested_floor = requested_floor
        self.direction = direction

    def get_floor(self):
        return self.requested_floor

    def get_direction(self):
        return self.direction

    def __eq__(self, other):
        return (
            isinstance(other, Request)
            and self.requested_floor == other.requested_floor
            and self.direction == other.direction
        )

    def __hash__(self):
        return hash((self.requested_floor, self.direction))

    def __repr__(self):
        return f"Request(floor={self.requested_floor}, direction={self.direction})"
