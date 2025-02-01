from math import floor
from time import mktime, localtime

BIN_WASTE = 'Waste'
BIN_RECYCLING = 'Recycle'
BIN_GARDEN = 'Garden'
BIN_FOOD = 'Food'

SECONDS_IN_DAY = 24 * 60 * 60

class Bin:
    name = "Undefined"
    start_time = 0
    period = 0

    def __init__(self, name, start_date, period):
        self.name = name
        self.start_time = start_date
        self.period = period

    def next_collection(self, t = None):
        if t is None:
            t = _normalise_time()
        difference = floor(t - self.start_time)
        days_since_start = difference // SECONDS_IN_DAY
        days_to_go = self.period - (days_since_start % self.period)
        day_offset = days_to_go % 7

        if days_to_go == self.period:
            # It's today, so still show today's date rather than the collection after
            days_to_go = 0

        is_next = days_to_go < 7

        next_time = self.start_time + (days_since_start + days_to_go) * SECONDS_IN_DAY
        (year, month, mday, hour, minute, second, weekday, yearday, dst) = _localtime(_normalise_time(next_time))
        return (year, month, mday, is_next)


def get_bin(name) -> Bin or None:
    for bin in bins:
        if bin.name == name:
            return bin
    return None

def get_all_bins() -> []:
    bin_list = []
    for bin in bins:
        (year, month, mday, is_next) = bin.next_collection()
        bin_list.append((bin.name, year, month, mday, is_next))
    return bin_list

def _normalise_time(t = None) -> float:
    (year, month, mday, hour, minute, second, weekday, yearday, dst) = _localtime(t)
    # Use 3am to get past GMT/BST switchovers
    return mktime((year, month, mday, 3, 0, 0, weekday, yearday, dst))

def _localtime(t = None):
    result = localtime(t)  # Get the localtime
    # Check if running in MicroPython by examining result length
    if len(result) == 8:  # MicroPython: 8 values
        year, month, mday, hour, minute, second, weekday, yearday = result
        dst = -1  # Default value for dst (e.g., -1 when undefined)
    elif len(result) == 9:  # Python: 9 values
        year, month, mday, hour, minute, second, weekday, yearday, dst = result
    else:
        raise ValueError("Unexpected localtime() return value")

    # Use year, month, mday, hour, minute, second, weekday, yearday, dst as needed
    return (year, month, mday, hour, minute, second, weekday, yearday, dst)

def _get_day_of_week(year, month, day) -> int:
    # Zeller's Congruence
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")
    if not (1 <= day <= 31):
        raise ValueError("Day must be a valid day of the month")

    if month < 3:
        month += 12
        year -= 1
    k = year % 100
    j = year // 100
    f = day + (13 * (month + 1)) // 5 + k + (k // 4) + (j // 4) - (2 * j)
    return (f + 5) % 7  # Map Saturday = 0 to Monday = 0


def _get_day_of_year(year, month, day) -> int:
    # Days in each month for non-leap years
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Check for a leap year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29  # February has 29 days in a leap year

    # Calculate day of year by summing full months and adding the day
    return sum(days_in_month[:month - 1]) + day
    
    
def _to_time(year, month, mday):
    # Use 3am to get past GMT/BST switchovers
    day_of_week = _get_day_of_week(year, month, mday)
    day_of_year = _get_day_of_year(year, month, mday)
    return mktime((year, month, mday, 3, 0, 0, day_of_week, day_of_year, -1))

bins = [
    Bin(BIN_WASTE, _to_time(2025, 1, 20), 21),
    Bin(BIN_RECYCLING, _to_time(2025, 1, 13), 14),
    Bin(BIN_GARDEN, _to_time(2025, 1, 6), 14),
    Bin(BIN_FOOD, _to_time(2025, 1, 6), 7)
]



if __name__ == '__main__':
    for bin in bins:
        # d = _to_time(2025, 1, 28)
        (year, month, mday, is_next)  = bin.next_collection()
        next = "Next" if is_next else ""
        print(f"{bin.name}: {mday}/{month}/{year} {next}")

