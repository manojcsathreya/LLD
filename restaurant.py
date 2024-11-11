from abc import ABC
from enum import Enum
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List


# Enum for Order Status
class OrderStatus(Enum):
    PENDING = 1
    PREPARING = 2
    READY = 3
    COMPLETED = 4
    CANCELLED = 5


# Enum for Payment Methods
class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2
    MOBILE_PAYMENT = 3


# Enum for Payment Status
class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3


# MenuItem class
class MenuItem:
    def __init__(self, id, name, description, price, available):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available = available

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def is_available(self):
        return self.available


# Order class
class Order:
    def __init__(self, id, items, total_amount, status, timestamp):
        self.id = id
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.timestamp = timestamp

    def set_status(self, status):
        self.status = status

    def get_id(self):
        return self.id

    def get_items(self):
        return self.items

    def get_total_amount(self):
        return self.total_amount

    def get_status(self):
        return self.status

    def get_timestamp(self):
        return self.timestamp


# Payment class
class Payment:
    def __init__(self, id, amount, method, status):
        self.id = id
        self.amount = amount
        self.method = method
        self.status = status

    def get_id(self):
        return self.id

    def get_amount(self):
        return self.amount

    def get_method(self):
        return self.method

    def get_status(self):
        return self.status


# Reservation class
class Reservation:
    def __init__(self, id, customer_name, contact_number, party_size, reservation_time):
        self.id = id
        self.customer_name = customer_name
        self.contact_number = contact_number
        self.party_size = party_size
        self.reservation_time = reservation_time


# Staff class
class Staff:
    def __init__(self, id, name, role, contact_number):
        self.id = id
        self.name = name
        self.role = role
        self.contact_number = contact_number


# Restaurant class implementing Singleton pattern
class Restaurant:
    _instance = None
    _lock = ThreadPoolExecutor(max_workers=1)

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.menu = []
        self.orders = {}
        self.reservations = []
        self.payments = {}
        self.staff = []

    def add_menu_item(self, item):
        self.menu.append(item)

    def remove_menu_item(self, item):
        self.menu.remove(item)

    def get_menu(self):
        return self.menu[:]

    def place_order(self, order):
        self.orders[order.get_id()] = order
        self._notify_kitchen(order)

    def update_order_status(self, order_id, status):
        order = self.orders.get(order_id)
        if order:
            order.set_status(status)
            self._notify_staff(order)

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def cancel_reservation(self, reservation):
        self.reservations.remove(reservation)

    def process_payment(self, payment):
        self.payments[payment.get_id()] = payment

    def add_staff(self, staff):
        self.staff.append(staff)

    def remove_staff(self, staff):
        self.staff.remove(staff)

    def _notify_kitchen(self, order):
        # Notify kitchen (this could be implemented further)
        pass

    def _notify_staff(self, order):
        # Notify staff (this could be implemented further)
        pass


# Restaurant Management Demo class to demonstrate the working of the system
class RestaurantManagementDemo:
    @staticmethod
    def run():
        restaurant = Restaurant()

        # Add menu items
        restaurant.add_menu_item(MenuItem(1, "Burger", "Delicious burger", 9.99, True))
        restaurant.add_menu_item(MenuItem(2, "Pizza", "Cheesy pizza", 12.99, True))
        restaurant.add_menu_item(MenuItem(3, "Salad", "Fresh salad", 7.99, True))

        # Place an order
        order = Order(1, [MenuItem(1, "Burger", "Delicious burger", 9.99, True),
                        MenuItem(3, "Salad", "Fresh salad", 7.99, True)],
                    17.98, OrderStatus.PENDING, datetime.now())
        restaurant.place_order(order)

        # Make a reservation
        reservation = Reservation(1, "John Doe", "1234567890", 4, datetime.now())
        restaurant.make_reservation(reservation)

        # Process a payment
        payment = Payment(1, 17.98, PaymentMethod.CREDIT_CARD, PaymentStatus.PENDING)
        restaurant.process_payment(payment)

        # Update order status
        restaurant.update_order_status(1, OrderStatus.PREPARING)
        restaurant.update_order_status(1, OrderStatus.READY)
        restaurant.update_order_status(1, OrderStatus.COMPLETED)

        # Add staff
        restaurant.add_staff(Staff(1, "Alice", "Manager", "9876543210"))
        restaurant.add_staff(Staff(2, "Bob", "Chef", "5432109876"))

        # Get menu
        menu = restaurant.get_menu()
        print("Menu:")
        for item in menu:
            print(f"{item.get_name()} - ${item.get_price():.2f}")


# Main entry point for running the demo
if __name__ == "__main__":
    RestaurantManagementDemo.run()
