import datetime
import threading
from abc import ABC, abstractmethod

# Account class
class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def get_account_number(self):
        return self.account_number

    def get_balance(self):
        return self.balance

    def debit(self, amount):
        self.balance -= amount

    def credit(self, amount):
        self.balance += amount


# Transaction base class
class Transaction(ABC):
    def __init__(self, transaction_id, account, amount):
        self.transaction_id = transaction_id
        self.account = account
        self.amount = amount

    @abstractmethod
    def execute(self):
        pass


# Deposit transaction
class DepositTransaction(Transaction):
    def __init__(self, transaction_id, account, amount):
        super().__init__(transaction_id, account, amount)

    def execute(self):
        self.account.credit(self.amount)


# Withdrawal transaction
class WithdrawalTransaction(Transaction):
    def __init__(self, transaction_id, account, amount):
        super().__init__(transaction_id, account, amount)

    def execute(self):
        self.account.debit(self.amount)


# CashDispenser class
class CashDispenser:
    def __init__(self, initial_cash):
        self.cash_available = initial_cash
        self.lock = threading.Lock()

    def dispense_cash(self, amount):
        with self.lock:
            if amount > self.cash_available:
                raise ValueError("Insufficient cash available in the ATM.")
            self.cash_available -= amount
            print(f"Cash dispensed: {amount}")


# Card class
class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin

    def get_card_number(self):
        return self.card_number

    def get_pin(self):
        return self.pin


# BankingService class
class BankingService:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, initial_balance):
        self.accounts[account_number] = Account(account_number, initial_balance)

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def process_transaction(self, transaction):
        transaction.execute()


# ATM class
class ATM:
    def __init__(self, banking_service, cash_dispenser):
        self.banking_service = banking_service
        self.cash_dispenser = cash_dispenser
        self.transaction_counter = 0
        self.transaction_lock = threading.Lock()

    def authenticate_user(self, card):
        # Authenticate user using card and PIN
        # This is a simple authentication method for now
        account = self.banking_service.get_account(card.get_card_number())
        if account is None:
            print("Authentication failed: Account not found.")
            return False
        # In real-world scenarios, PIN verification would happen here
        print(f"User {card.get_card_number()} authenticated.")
        return True

    def check_balance(self, account_number):
        account = self.banking_service.get_account(account_number)
        if account:
            return account.get_balance()
        return None

    def withdraw_cash(self, account_number, amount):
        account = self.banking_service.get_account(account_number)
        if account and account.get_balance() >= amount:
            transaction = WithdrawalTransaction(self.generate_transaction_id(), account, amount)
            self.banking_service.process_transaction(transaction)
            self.cash_dispenser.dispense_cash(amount)
        else:
            print("Insufficient funds or account not found.")

    def deposit_cash(self, account_number, amount):
        account = self.banking_service.get_account(account_number)
        if account:
            transaction = DepositTransaction(self.generate_transaction_id(), account, amount)
            self.banking_service.process_transaction(transaction)
        else:
            print("Account not found.")

    def generate_transaction_id(self):
        with self.transaction_lock:
            self.transaction_counter += 1
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            return f"TXN{timestamp}{self.transaction_counter:010d}"


# ATM demo class
class ATMDemo:
    @staticmethod
    def run():
        banking_service = BankingService()
        cash_dispenser = CashDispenser(10000)
        atm = ATM(banking_service, cash_dispenser)

        # Create sample accounts
        banking_service.create_account("1234567890", 1000.0)
        banking_service.create_account("9876543210", 500.0)

        # Perform ATM operations
        card = Card("1234567890", "1234")
        if atm.authenticate_user(card):
            balance = atm.check_balance("1234567890")
            print(f"Account balance: {balance}")

            atm.withdraw_cash("1234567890", 500.0)
            atm.deposit_cash("9876543210", 200.0)

            balance = atm.check_balance("1234567890")
            print(f"Updated account balance: {balance}")

if __name__ == "__main__":
    ATMDemo.run()
