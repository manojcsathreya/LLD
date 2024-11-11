from datetime import datetime, timedelta
from threading import Lock
from enum import Enum
from typing import List

class SeatStatus(Enum):
    AVAILABLE = 1
    RESERVED = 2
    OCCUPIED = 3

class SeatType(Enum):
    ECONOMY = 1
    PREMIUM_ECONOMY = 2
    BUSINESS = 3
    FIRST_CLASS = 4

class Seat:
    def __init__(self, seat_number, seat_type):
        self.seat_number = seat_number
        self.type = seat_type
        self.status = SeatStatus.AVAILABLE

    def reserve(self):
        if self.status == SeatStatus.AVAILABLE:
            self.status = SeatStatus.RESERVED
        else:
            raise ValueError("Seat cannot be reserved")

    def release(self):
        if self.status == SeatStatus.RESERVED:
            self.status = SeatStatus.AVAILABLE
        else:
            raise ValueError("Seat was not reserved")

class Flight:
    def __init__(self, flight_number, source, destination, departure_time, arrival_time, total_seats):
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats = [Seat(f"{i+1}{chr(65 + i % 26)}", SeatType.ECONOMY) for i in range(total_seats)]

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination

    def get_departure_time(self):
        return self.departure_time

    def get_seats(self):
        return self.seats

class BookingStatus(Enum):
    CONFIRMED = 1
    CANCELLED = 2
    PENDING = 3
    EXPIRED = 4

class Booking:
    def __init__(self, booking_number, flight, passenger, seat, price):
        self.booking_number = booking_number
        self.flight = flight
        self.passenger = passenger
        self.seat = seat
        self.price = price
        self.status = BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CANCELLED
        self.seat.release()

class BookingManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.bookings = {}
        self.booking_counter = 0

    def create_booking(self, flight, passenger, seat, price):
        booking_number = self._generate_booking_number()
        booking = Booking(booking_number, flight, passenger, seat, price)
        with self._lock:
            self.bookings[booking_number] = booking
        seat.reserve()
        return booking

    def cancel_booking(self, booking_number):
        with self._lock:
            booking = self.bookings.get(booking_number)
            if booking:
                booking.cancel()

    def _generate_booking_number(self):
        self.booking_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BKG{timestamp}{self.booking_counter:06d}"

class AirlineManagementSystem:
    def __init__(self):
        self.flights = []
        self.booking_manager = BookingManager()

    def add_flight(self, flight):
        self.flights.append(flight)

    def search_flights(self, source, destination, date):
        return [flight for flight in self.flights
                if flight.get_source().lower() == source.lower()
                and flight.get_destination().lower() == destination.lower()
                and flight.get_departure_time().date() == date]

    def book_flight(self, flight, passenger, seat, price):
        return self.booking_manager.create_booking(flight, passenger, seat, price)

    def cancel_booking(self, booking_number):
        self.booking_manager.cancel_booking(booking_number)

class AirlineManagementSystemDemo:
    @staticmethod
    def run():
        system = AirlineManagementSystem()
        passenger = "John Doe"  # Simplified passenger for demo

        # Create flights
        departure_time1 = datetime.now() + timedelta(days=1)
        arrival_time1 = departure_time1 + timedelta(hours=2)
        flight1 = Flight("F001", "New York", "London", departure_time1, arrival_time1, total_seats=50)

        system.add_flight(flight1)

        # Search flights
        search_results = system.search_flights("New York", "London", departure_time1.date())
        print(f"Flights found: {len(search_results)}")

        # Book a flight
        seat = flight1.get_seats()[0]  # Select first available seat
        booking = system.book_flight(flight1, passenger, seat, 200)
        print(f"Booking successful: {booking.booking_number}")

        # Cancel the booking
        system.cancel_booking(booking.booking_number)
        print(f"Booking {booking.booking_number} cancelled.")

if __name__ == "__main__":
    AirlineManagementSystemDemo.run()
