from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict
import itertools

# Enum definitions
class BookingStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"

class SeatType(Enum):
    NORMAL = "NORMAL"
    PREMIUM = "PREMIUM"

# Movie class
class Movie:
    def __init__(self, movie_id: str, title: str, description: str, duration_in_minutes: int):
        self._id = movie_id
        self._title = title
        self._description = description
        self._duration_in_minutes = duration_in_minutes

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def duration_in_minutes(self) -> int:
        return self._duration_in_minutes

# User class
class User:
    def __init__(self, user_id: str, name: str, email: str):
        self._id = user_id
        self._name = name
        self._email = email

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

# Seat class
class Seat:
    def __init__(self, seat_id: str, row: int, column: int, seat_type: SeatType, price: float, status: SeatStatus):
        self._id = seat_id
        self._row = row
        self._column = column
        self._type = seat_type
        self._price = price
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def type(self) -> SeatType:
        return self._type

    @property
    def price(self) -> float:
        return self._price

    @property
    def status(self) -> SeatStatus:
        return self._status

    @status.setter
    def status(self, status: SeatStatus):
        self._status = status

# Theater class
class Theater:
    def __init__(self, theater_id: str, name: str, location: str, shows: List):
        self._id = theater_id
        self._name = name
        self._location = location
        self._shows = shows

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> str:
        return self._location

    @property
    def shows(self) -> List:
        return self._shows

# Show class
class Show:
    def __init__(self, show_id: str, movie: Movie, theater: Theater, start_time: datetime, end_time: datetime, seats: Dict[str, Seat]):
        self._id = show_id
        self._movie = movie
        self._theater = theater
        self._start_time = start_time
        self._end_time = end_time
        self._seats = seats

    @property
    def id(self) -> str:
        return self._id

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def theater(self) -> Theater:
        return self._theater

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @property
    def seats(self) -> Dict[str, Seat]:
        return self._seats

# Booking class
class Booking:
    def __init__(self, booking_id: str, user: User, show: Show, seats: List[Seat], total_price: float, status: BookingStatus):
        self._id = booking_id
        self._user = user
        self._show = show
        self._seats = seats
        self._total_price = total_price
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> User:
        return self._user

    @property
    def show(self) -> Show:
        return self._show

    @property
    def seats(self) -> List[Seat]:
        return self._seats

    @property
    def total_price(self) -> float:
        return self._total_price

    @property
    def status(self) -> BookingStatus:
        return self._status

    @status.setter
    def status(self, status: BookingStatus):
        self._status = status

# MovieTicketBookingSystem class (Singleton)
class MovieTicketBookingSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.movies = []
            cls._instance.theaters = []
            cls._instance.shows = {}
            cls._instance.bookings = {}
            cls._instance.booking_counter = itertools.count(1)
        return cls._instance

    @staticmethod
    def get_instance():
        if MovieTicketBookingSystem._instance is None:
            MovieTicketBookingSystem()
        return MovieTicketBookingSystem._instance

    def add_movie(self, movie: Movie):
        self.movies.append(movie)

    def add_theater(self, theater: Theater):
        self.theaters.append(theater)

    def add_show(self, show: Show):
        self.shows[show.id] = show

    def get_movies(self) -> List[Movie]:
        return self.movies

    def get_theaters(self) -> List[Theater]:
        return self.theaters

    def get_show(self, show_id: str) -> Show:
        return self.shows.get(show_id)

    def book_tickets(self, user: User, show: Show, selected_seats: List[Seat]) -> Booking:
        if self._are_seats_available(show, selected_seats):
            self._mark_seats_as_booked(show, selected_seats)
            total_price = self._calculate_total_price(selected_seats)
            booking_id = self._generate_booking_id()
            booking = Booking(booking_id, user, show, selected_seats, total_price, BookingStatus.PENDING)
            self.bookings[booking_id] = booking
            return booking
        return None

    def _are_seats_available(self, show: Show, selected_seats: List[Seat]) -> bool:
        for seat in selected_seats:
            show_seat = show.seats.get(seat.id)
            if show_seat is None or show_seat.status != SeatStatus.AVAILABLE:
                return False
        return True

    def _mark_seats_as_booked(self, show: Show, selected_seats: List[Seat]):
        for seat in selected_seats:
            show_seat = show.seats.get(seat.id)
            show_seat.status = SeatStatus.BOOKED

    def _calculate_total_price(self, selected_seats: List[Seat]) -> float:
        return sum(seat.price for seat in selected_seats)

    def _generate_booking_id(self) -> str:
        booking_number = next(self._instance.booking_counter)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BKG{timestamp}{booking_number:06d}"

    def confirm_booking(self, booking_id: str):
        booking = self.bookings.get(booking_id)
        if booking and booking.status == BookingStatus.PENDING:
            booking.status = BookingStatus.CONFIRMED

    def cancel_booking(self, booking_id: str):
        booking = self.bookings.get(booking_id)
        if booking and booking.status != BookingStatus.CANCELLED:
            booking.status = BookingStatus.CANCELLED
            self._mark_seats_as_available(booking.show, booking.seats)

    def _mark_seats_as_available(self, show: Show, seats: List[Seat]):
        for seat in seats:
            show_seat = show.seats.get(seat.id)
            show_seat.status = SeatStatus.AVAILABLE

# Utility to create seats
def create_seats(rows, columns):
    seats = {}
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            seat_id = f"{row}-{col}"
            seat_type = SeatType.PREMIUM if row <= 2 else SeatType.NORMAL
            price = 150.0 if seat_type == SeatType.PREMIUM else 100.0
            seat = Seat(seat_id, row, col, seat_type, price, SeatStatus.AVAILABLE)
            seats[seat_id] = seat
    return seats

# Demo class to test the booking system
class MovieTicketBookingDemo:
    def run_demo(self):
        system = MovieTicketBookingSystem.get_instance()
        movie = Movie("M1", "Inception", "A sci-fi thriller", 148)
        theater = Theater("T1", "Main Street Cinema", "123 Main St", [])
        seats = create_seats(5, 10)
        show = Show("S1", movie, theater, datetime.now(), datetime.now() + timedelta(hours=2), seats)
        
        system.add_movie(movie)
        system.add_theater(theater)
        system.add_show(show)
        
        user = User("U1", "John Doe", "johndoe@example.com")
        selected_seats = [seats["1-1"], seats["1-2"]]
        
        booking = system.book_tickets(user, show, selected_seats)
        if booking:
            print("Booking ID:", booking.id)
            print("Total Price:", booking.total_price)
            system.confirm_booking(booking.id)
            print("Booking confirmed.")

# Running demo
if __name__ == "__main__":
    demo = MovieTicketBookingDemo()
    demo.run_demo()