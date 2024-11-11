import uuid
from typing import List, Dict
from enum import Enum
from abc import ABC, abstractmethod

# ----- Order Status Enum -----
class OrderStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

# ----- Payment Abstract Base Class -----
class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

# ----- CreditCardPayment Class -----
class CreditCardPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        # Process credit card payment (stub implementation)
        return True

# ----- Product Class -----
class Product:
    def __init__(self, product_id: str, name: str, description: str, price: float, quantity: int):
        self._id = product_id
        self._name = name
        self._description = description
        self._price = price
        self._quantity = quantity

    def update_quantity(self, quantity: int):
        self._quantity += quantity

    def is_available(self, quantity: int) -> bool:
        return self._quantity >= quantity

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def price(self) -> float:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

# ----- OrderItem Class -----
class OrderItem:
    def __init__(self, product, quantity: int):
        self._product = product
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

# ----- Order Class -----
class Order:
    def __init__(self, order_id: str, user, items: List[OrderItem], total_amount: float):
        self._id = order_id
        self._user = user
        self._items = items
        self._total_amount = total_amount
        self._status = OrderStatus.PENDING

    def calculate_total_amount(self) -> float:
        return sum(item.product.price * item.quantity for item in self._items)

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self):
        return self._user

    @property
    def items(self) -> List[OrderItem]:
        return self._items

    @property
    def total_amount(self) -> float:
        return self._total_amount

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

# ----- ShoppingCart Class -----
class ShoppingCart:
    def __init__(self):
        self._items: Dict[str, OrderItem] = {}

    def add_item(self, product: Product, quantity: int):
        product_id = product.id
        if product_id in self._items:
            item = self._items[product_id]
            quantity += item.quantity
        self._items[product_id] = OrderItem(product, quantity)

    def remove_item(self, product_id: str):
        if product_id in self._items:
            del self._items[product_id]

    def update_item_quantity(self, product_id: str, quantity: int):
        if product_id in self._items:
            item = self._items[product_id]
            self._items[product_id] = OrderItem(item.product, quantity)

    def get_items(self) -> List[OrderItem]:
        return list(self._items.values())

    def clear(self):
        self._items.clear()

# ----- User Class -----
class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        self._id = user_id
        self._name = name
        self._email = email
        self._password = password
        self._orders = []

    def add_order(self, order):
        self._orders.append(order)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @property
    def orders(self) -> List:
        return self._orders

# ----- OnlineShoppingService Class -----
class OnlineShoppingService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = {}
            cls._instance.products = {}
            cls._instance.orders = {}
        return cls._instance

    def register_user(self, user: User):
        self.users[user.id] = user

    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)

    def add_product(self, product: Product):
        self.products[product.id] = product

    def get_product(self, product_id: str) -> Product:
        return self.products.get(product_id)

    def search_products(self, keyword: str) -> List[Product]:
        return [product for product in self.products.values() if keyword.lower() in product.name.lower()]

    def place_order(self, user: User, cart: ShoppingCart, payment: Payment) -> Order:
        order_items = []
        for item in cart.get_items():
            product = item.product
            quantity = item.quantity
            if product.is_available(quantity):
                product.update_quantity(-quantity)
                order_items.append(item)

        if not order_items:
            raise Exception("No available products in the cart.")

        order_id = self._generate_order_id()
        order = Order(order_id, user, order_items, self._calculate_total_amount(order_items))
        self.orders[order_id] = order
        user.add_order(order)
        cart.clear()

        if payment.process_payment(order.total_amount):
            order.status = OrderStatus.PROCESSING
        else:
            order.status = OrderStatus.CANCELLED
            for item in order_items:
                item.product.update_quantity(item.quantity)

        return order

    def get_order(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def _generate_order_id(self) -> str:
        return "ORDER" + str(uuid.uuid4()).split('-')[0].upper()

    def _calculate_total_amount(self, items: List) -> float:
        return sum(item.product.price * item.quantity for item in items)

# ----- OnlineShoppingServiceDemo Class -----
class OnlineShoppingServiceDemo:
    @staticmethod
    def run():
        shopping_service = OnlineShoppingService()

        # Register users
        user1 = User("U001", "John Doe", "john@example.com", "password123")
        user2 = User("U002", "Jane Smith", "jane@example.com", "password456")
        shopping_service.register_user(user1)
        shopping_service.register_user(user2)

        # Add products
        product1 = Product("P001", "Smartphone", "High-end smartphone", 999.99, 10)
        product2 = Product("P002", "Laptop", "Powerful gaming laptop", 1999.99, 5)
        shopping_service.add_product(product1)
        shopping_service.add_product(product2)

        # User 1 adds products to cart and places an order
        cart1 = ShoppingCart()
        cart1.add_item(product1, 2)
        cart1.add_item(product2, 1)
        payment1 = CreditCardPayment()
        order1 = shopping_service.place_order(user1, cart1, payment1)
        print("Order placed:", order1.id)

        # User 2 searches for products and adds to cart
        search_results = shopping_service.search_products("laptop")
        print("Search Results:")
        for product in search_results:
            print(product.name)

        cart2 = ShoppingCart()
        cart2.add_item(search_results[0], 1)
        payment2 = CreditCardPayment()
        order2 = shopping_service.place_order(user2, cart2, payment2)
        print("Order placed:", order2.id)

        # User 1 views order history
        user_orders = user1.orders
        print("User 1 Order History:")
        for order in user_orders:
            print("Order ID:", order.id)
            print("Total Amount: $", order.total_amount)
            print("Status:", order.status)

if __name__ == "__main__":
    OnlineShoppingServiceDemo.run()
