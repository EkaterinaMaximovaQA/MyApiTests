
from enum import Enum

class BookingEndpoints(Enum):
    # Healthcheck
    PING = "/ping"

    # Authentication
    AUTH = "/auth"

    # Bookings
    BOOKING = "/booking"

