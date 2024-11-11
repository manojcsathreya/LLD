from enum import Enum
from queue import Queue
from threading import Lock


# Exception classes
class InsufficientFundsException(Exception):
    pass

class InsufficientStockException(Exception):
    pass


# Enum for Order Status
class OrderStatus(Enum):
    PENDING = 0
    EXECUTED = 1
    REJECTED = 2


# Portfolio class to manage the stock holdings of an account
class Portfolio:
    def __init__(self, account):
        self.account = account
        self.holdings = {}

    def add_stock(self, stock, quantity):
        symbol = stock.get_symbol()
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

    def remove_stock(self, stock, quantity):
        symbol = stock.get_symbol()
        if symbol in self.holdings:
            current_quantity = self.holdings[symbol]
            if current_quantity > quantity:
                self.holdings[symbol] = current_quantity - quantity
            elif current_quantity == quantity:
                del self.holdings[symbol]
            else:
                raise InsufficientStockException("Insufficient stock quantity in the portfolio.")
        else:
            raise InsufficientStockException("Stock not found in the portfolio.")

    def get_holdings(self):
        return self.holdings


# Stock class to represent individual stocks
class Stock:
    def __init__(self, symbol, name, price):
        self.symbol = symbol
        self.name = name
        self.price = price

    def update_price(self, new_price):
        self.price = new_price

    def get_symbol(self):
        return self.symbol

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price


# Order class, base class for buy and sell orders
class Order:
    def __init__(self, order_id, account, stock, quantity, price):
        self.order_id = order_id
        self.account = account
        self.stock = stock
        self.quantity = quantity
        self.price = price
        self.status = OrderStatus.PENDING

    def execute(self):
        pass


# BuyOrder class for executing buy orders
class BuyOrder(Order):
    def __init__(self, order_id, account, stock, quantity, price):
        super().__init__(order_id, account, stock, quantity, price)

    def execute(self):
        total_cost = self.quantity * self.price
        if self.account.get_balance() >= total_cost:
            self.account.withdraw(total_cost)
            self.account.get_portfolio().add_stock(self.stock, self.quantity)
            self.status = OrderStatus.EXECUTED
        else:
            self.status = OrderStatus.REJECTED
            raise InsufficientFundsException("Insufficient funds to execute the buy order.")


# SellOrder class for executing sell orders
class SellOrder(Order):
    def __init__(self, order_id, account, stock, quantity, price):
        super().__init__(order_id, account, stock, quantity, price)

    def execute(self):
        total_proceeds = self.quantity * self.price
        if self.account.get_portfolio().get_holdings().get(self.stock.get_symbol(), 0) >= self.quantity:
            self.account.get_portfolio().remove_stock(self.stock, self.quantity)
            self.account.deposit(total_proceeds)
            self.status = OrderStatus.EXECUTED
        else:
            self.status = OrderStatus.REJECTED
            raise InsufficientStockException("Insufficient stock to execute the sell order.")


# Account class representing a user's brokerage account
class Account:
    def __init__(self, account_id, user, initial_balance):
        self.account_id = account_id
        self.user = user
        self.balance = initial_balance
        self.portfolio = Portfolio(self)

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise InsufficientFundsException("Insufficient funds in the account.")

    def get_balance(self):
        return self.balance

    def get_portfolio(self):
        return self.portfolio


# StockBroker class for managing accounts, stocks, and orders
class StockBroker:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.accounts = {}
                    cls._instance.stocks = {}
                    cls._instance.order_queue = Queue()
                    cls._instance.account_id_counter = 1
        return cls._instance

    def create_account(self, user, initial_balance):
        account_id = self._generate_account_id()
        account = Account(account_id, user, initial_balance)
        self.accounts[account_id] = account

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def add_stock(self, stock):
        self.stocks[stock.get_symbol()] = stock

    def get_stock(self, symbol):
        return self.stocks.get(symbol)

    def place_order(self, order):
        self.order_queue.put(order)
        self._process_orders()

    def _process_orders(self):
        while not self.order_queue.empty():
            order = self.order_queue.get()
            try:
                order.execute()
            except (InsufficientFundsException, InsufficientStockException) as e:
                # Handle exception and notify user
                print(f"Order failed: {str(e)}")

    def _generate_account_id(self):
        account_id = self.account_id_counter
        self.account_id_counter += 1
        return f"A{account_id:09d}"


# User class representing a customer using the brokerage system
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email


# StockBrokerageSystemDemo class to run a demo of the system
class StockBrokerageSystemDemo:
    @staticmethod
    def run():
        stock_broker = StockBroker()

        # Create user and account
        user = User("U001", "John Doe", "john@example.com")
        stock_broker.create_account(user, 10000.0)
        account = stock_broker.get_account("A000000001")

        # Add stocks to the stock broker
        stock1 = Stock("AAPL", "Apple Inc.", 150.0)
        stock2 = Stock("GOOGL", "Alphabet Inc.", 2000.0)
        stock_broker.add_stock(stock1)
        stock_broker.add_stock(stock2)

        # Place buy orders
        buy_order1 = BuyOrder("O001", account, stock1, 10, 150.0)
        buy_order2 = BuyOrder("O002", account, stock2, 5, 2000.0)
        stock_broker.place_order(buy_order1)
        stock_broker.place_order(buy_order2)

        # Place sell orders
        sell_order1 = SellOrder("O003", account, stock1, 5, 160.0)
        stock_broker.place_order(sell_order1)

        # Print account balance and portfolio
        print(f"Account Balance: ${account.get_balance()}")
        print(f"Portfolio: {account.get_portfolio().get_holdings()}")


if __name__ == "__main__":
    StockBrokerageSystemDemo.run()
