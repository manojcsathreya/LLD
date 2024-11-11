from enum import Enum
from abc import ABC, abstractmethod
from threading import Lock
import time

# Define Coin and Note as enums
class Coin(Enum):
    PENNY = 0.01
    NICKEL = 0.05
    DIME = 0.1
    QUARTER = 0.25

class Note(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20

# Define Product
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Define Inventory
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity):
        self.products[product] = quantity

    def remove_product(self, product):
        del self.products[product]

    def update_quantity(self, product, quantity):
        self.products[product] = quantity

    def get_quantity(self, product):
        return self.products.get(product, 0)

    def is_available(self, product):
        return product in self.products and self.products[product] > 0

# Define VendingMachineState (Abstract Base Class for States)
class VendingMachineState(ABC):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    @abstractmethod
    def select_product(self, product):
        pass

    @abstractmethod
    def insert_coin(self, coin):
        pass

    @abstractmethod
    def insert_note(self, note):
        pass

    @abstractmethod
    def dispense_product(self):
        pass

    @abstractmethod
    def return_change(self):
        pass

# Define Concrete States
class IdleState(VendingMachineState):
    def select_product(self, product: Product):
        if self.vending_machine.inventory.is_available(product):
            self.vending_machine.selected_product = product
            self.vending_machine.set_state(self.vending_machine.ready_state)
            print(f"Product selected: {product.name}")
        else:
            print(f"Product not available: {product.name}")

    def insert_coin(self, coin: Coin):
        print("Please select a product first.")

    def insert_note(self, note: Note):
        print("Please select a product first.")

    def dispense_product(self):
        print("Please select a product and make payment.")

    def return_change(self):
        print("No change to return.")

class ReadyState(VendingMachineState):
    def select_product(self, product: Product):
        print("Product already selected. Please make payment.")

    def insert_coin(self, coin: Coin):
        self.vending_machine.add_coin(coin)
        print(f"Coin inserted: {coin.name}")
        self.check_payment_status()

    def insert_note(self, note: Note):
        self.vending_machine.add_note(note)
        print(f"Note inserted: {note.name}")
        self.check_payment_status()

    def dispense_product(self):
        print("Please make payment first.")

    def return_change(self):
        change = self.vending_machine.total_payment - self.vending_machine.selected_product.price
        if change > 0:
            print(f"Change returned: ${change:.2f}")
            self.vending_machine.reset_payment()
        else:
            print("No change to return.")
        self.vending_machine.set_state(self.vending_machine.idle_state)

    def check_payment_status(self):
        if self.vending_machine.total_payment >= self.vending_machine.selected_product.price:
            self.vending_machine.set_state(self.vending_machine.dispense_state)

class DispenseState(VendingMachineState):
    def select_product(self, product: Product):
        print("Product already selected. Please collect the dispensed product.")

    def insert_coin(self, coin: Coin):
        print("Payment already made. Please collect the dispensed product.")

    def insert_note(self, note: Note):
        print("Payment already made. Please collect the dispensed product.")

    def dispense_product(self):
        product = self.vending_machine.selected_product
        self.vending_machine.inventory.update_quantity(product, self.vending_machine.inventory.get_quantity(product) - 1)
        print(f"Product dispensed: {product.name}")
        self.vending_machine.set_state(self.vending_machine.return_change_state)

    def return_change(self):
        print("Please collect the dispensed product first.")

class ReturnChangeState(VendingMachineState):
    def select_product(self, product: Product):
        print("Please collect the change first.")

    def insert_coin(self, coin: Coin):
        print("Please collect the change first.")

    def insert_note(self, note: Note):
        print("Please collect the change first.")

    def dispense_product(self):
        print("Product already dispensed. Please collect the change.")

    def return_change(self):
        change = self.vending_machine.total_payment - self.vending_machine.selected_product.price
        if change > 0:
            print(f"Change returned: ${change:.2f}")
            self.vending_machine.reset_payment()
        else:
            print("No change to return.")
        self.vending_machine.reset_selected_product()
        self.vending_machine.set_state(self.vending_machine.idle_state)

# Define the VendingMachine
class VendingMachine:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.inventory = Inventory()
                cls._instance.idle_state = IdleState(cls._instance)
                cls._instance.ready_state = ReadyState(cls._instance)
                cls._instance.dispense_state = DispenseState(cls._instance)
                cls._instance.return_change_state = ReturnChangeState(cls._instance)
                cls._instance.current_state = cls._instance.idle_state
                cls._instance.selected_product = None
                cls._instance.total_payment = 0.0
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def select_product(self, product: Product):
        self.current_state.select_product(product)

    def insert_coin(self, coin: Coin):
        self.current_state.insert_coin(coin)

    def insert_note(self, note: Note):
        self.current_state.insert_note(note)

    def dispense_product(self):
        self.current_state.dispense_product()

    def return_change(self):
        self.current_state.return_change()

    def set_state(self, state: VendingMachineState):
        self.current_state = state

    def add_coin(self, coin: Coin):
        self.total_payment += coin.value

    def add_note(self, note: Note):
        self.total_payment += note.value

    def reset_payment(self):
        self.total_payment = 0.0

    def reset_selected_product(self):
        self.selected_product = None

# Run the Vending Machine Demo
class VendingMachineDemo:
    @staticmethod
    def run():
        vending_machine = VendingMachine.get_instance()

        # Add products to the inventory
        coke = Product("Coke", 1.5)
        pepsi = Product("Pepsi", 1.5)
        water = Product("Water", 1.0)

        vending_machine.inventory.add_product(coke, 5)
        vending_machine.inventory.add_product(pepsi, 3)
        vending_machine.inventory.add_product(water, 2)

        # Example usage
        vending_machine.select_product(coke)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_note(Note.ONE)
        vending_machine.dispense_product()
        vending_machine.return_change()

if __name__ == "__main__":
    VendingMachineDemo.run()
