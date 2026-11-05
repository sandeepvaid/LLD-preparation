from strategy.fare_strategy import FareStrategy


class PeakHoursFareStrategy(FareStrategy):
    PEAK_HOURS_MULTIPLIER = 1.5
    PEAK_HOURS = {8, 9, 10, 17, 18, 19}   # 8-10am, 5-7pm

    def calculate_fare(self, ticket, current_fare: float) -> float:
        if ticket.entry_time.hour in self.PEAK_HOURS:
            return current_fare * self.PEAK_HOURS_MULTIPLIER
        return current_fare
