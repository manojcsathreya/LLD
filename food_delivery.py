from enum import Enum
from typing import List, Dict
from uuid import uuid4
from threading import Lock
import time

# Enums
class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


# Core Classes
class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.id = customer_id
        self.name = name
        self.email = email
        self.phone = phone


class DeliveryAgent:
    def __init__(self, agent_id: str, name: str, phone: str):
        self.id = agent_id
        self.name = name
        self.phone = phone
        self.available = True
        self.lock = Lock()  # Individual lock for each agent


class Restaurant:
    def __init__(self, restaurant_id: str, name: str, address: str, menu: Dict[str, float]):
        self.id = restaurant_id
        self.name = name
        self.address = address
        self.menu = menu  # Dictionary of item name to price


class Order:
    def __init__(self, order_id: str, customer: Customer, restaurant: Restaurant, items: Dict[str, int]):
        self.id = order_id
        self.customer = customer
        self.restaurant = restaurant
        self.items = items  # Dictionary of item name to quantity
        self.status = OrderStatus.PENDING
        self.delivery_agent = None
        self.lock = Lock()  # Lock for each order to prevent simultaneous status changes

    def set_status(self, status: OrderStatus):
        with self.lock:
            self.status = status

    def assign_delivery_agent(self, agent: DeliveryAgent):
        with agent.lock:
            agent.available = False
        with self.lock:
            self.delivery_agent = agent


# Singleton Service Class
class FoodDeliveryService:
    _instance = None
    _instance_lock = Lock()  # Lock for singleton instance creation

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.customers = {}
                cls._instance.restaurants = {}
                cls._instance.orders = {}
                cls._instance.delivery_agents = {}
                cls._instance.locks = {
                    "customers": Lock(),
                    "restaurants": Lock(),
                    "orders": Lock(),
                    "delivery_agents": Lock(),
                }
        return cls._instance

    @staticmethod
    def get_instance():
        if FoodDeliveryService._instance is None:
            FoodDeliveryService()
        return FoodDeliveryService._instance

    def register_customer(self, customer: Customer):
        with self.locks["customers"]:
            self.customers[customer.id] = customer

    def register_restaurant(self, restaurant: Restaurant):
        with self.locks["restaurants"]:
            self.restaurants[restaurant.id] = restaurant

    def register_delivery_agent(self, agent: DeliveryAgent):
        with self.locks["delivery_agents"]:
            self.delivery_agents[agent.id] = agent

    def get_available_restaurants(self) -> List[Restaurant]:
        with self.locks["restaurants"]:
            return list(self.restaurants.values())

    def place_order(self, customer_id: str, restaurant_id: str, items: Dict[str, int]) -> Order:
        with self.locks["customers"], self.locks["restaurants"]:
            customer = self.customers.get(customer_id)
            restaurant = self.restaurants.get(restaurant_id)
            if customer and restaurant:
                order = Order(self.generate_order_id(), customer, restaurant, items)
                with self.locks["orders"]:
                    self.orders[order.id] = order
                # Notify restaurant about new order
                return order
        return None

    def update_order_status(self, order_id: str, status: OrderStatus):
        with self.locks["orders"]:
            order = self.orders.get(order_id)
            if order:
                order.set_status(status)
                # Notify customer and restaurant about order status update
                if status == OrderStatus.CONFIRMED:
                    self.assign_delivery_agent(order)

    def cancel_order(self, order_id: str):
        with self.locks["orders"]:
            order = self.orders.get(order_id)
            if order and order.status == OrderStatus.PENDING:
                order.set_status(OrderStatus.CANCELLED)
                # Notify customer and restaurant about cancellation

    def assign_delivery_agent(self, order: Order):
        with self.locks["delivery_agents"]:
            for agent in self.delivery_agents.values():
                with agent.lock:
                    if agent.available:
                        order.assign_delivery_agent(agent)
                        # Notify delivery agent about the assigned order
                        break

    def generate_order_id(self) -> str:
        return "ORD" + uuid4().hex[:8].upper()


# Demo
class FoodDeliveryServiceDemo:
    @staticmethod
    def run():
        service = FoodDeliveryService.get_instance()

        # Register customers
        customer1 = Customer("C001", "Alice Johnson", "alice@example.com", "555-1234")
        customer2 = Customer("C002", "Bob Smith", "bob@example.com", "555-5678")
        service.register_customer(customer1)
        service.register_customer(customer2)

        # Register restaurants with menu
        restaurant1 = Restaurant("R001", "Pizza Place", "123 Main St", {"Pizza": 10.0, "Burger": 8.0})
        restaurant2 = Restaurant("R002", "Sushi House", "456 Oak St", {"Sushi": 12.0, "Ramen": 15.0})
        service.register_restaurant(restaurant1)
        service.register_restaurant(restaurant2)

        # Register delivery agents
        agent1 = DeliveryAgent("D001", "Charlie Brown", "555-8765")
        agent2 = DeliveryAgent("D002", "Daisy Duck", "555-4321")
        service.register_delivery_agent(agent1)
        service.register_delivery_agent(agent2)

        # Place an order
        items = {"Pizza": 2, "Burger": 1}
        order = service.place_order(customer1.id, restaurant1.id, items)
        if order:
            print(f"Order placed: {order.id}")

        # Update order status to confirmed and assign delivery agent
        service.update_order_status(order.id, OrderStatus.CONFIRMED)
        print(f"Order status updated to {OrderStatus.CONFIRMED}")

        # Cancel an order
        service.cancel_order(order.id)
        print(f"Order cancelled: {order.id}")


if __name__ == "__main__":
    FoodDeliveryServiceDemo.run()
