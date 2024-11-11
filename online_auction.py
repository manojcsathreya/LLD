import threading
from enum import Enum
from typing import List, Optional
import datetime

# Enum for Auction Status
class AuctionStatus(Enum):
    ACTIVE = 1
    CLOSED = 2

# Bid Class
class Bid:
    def __init__(self, bid_id, bidder, amount):
        self.id = bid_id
        self.bidder = bidder
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def get_amount(self):
        return self.amount

    def get_bidder(self):
        return self.bidder

# User Class
class User:
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    def get_id(self):
        return self.id


# Auction Listing Class
class AuctionListing:
    def __init__(self, id: str, item_name: str, description: str, starting_price: float, duration: int, seller: User):
        self.id = id
        self.item_name = item_name
        self.description = description
        self.starting_price = starting_price
        self.duration = duration
        self.seller = seller
        self.status = AuctionStatus.ACTIVE
        self.current_highest_bid = starting_price
        self.current_highest_bidder: Optional[User] = None
        self.bids: List[Bid] = []
        self.lock = threading.Lock()

        # Start a timer to automatically close the auction after the specified duration
        threading.Timer(self.duration, self.close_auction).start()

    def place_bid(self, bid: Bid):
        with self.lock:
            if self.status == AuctionStatus.ACTIVE and bid.amount > self.current_highest_bid:
                self.current_highest_bid = bid.amount
                self.current_highest_bidder = bid.bidder
                self.bids.append(bid)
                self.notify_observers()
                print(f"Bid placed: {bid.amount} by {bid.bidder.username} for {self.item_name}")
            else:
                print(f"Bid rejected: {bid.amount} by {bid.bidder.username} for {self.item_name}")


    def close_auction(self):
        with self.lock:
            if self.status == AuctionStatus.ACTIVE:
                self.status = AuctionStatus.CLOSED
                self.notify_observers()

    def notify_observers(self):
        pass

    
# Auction System Class
class AuctionSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = {}
            cls._instance.auction_listings = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def register_user(self, user: User):
        self.users[user.id] = user

    def create_auction_listing(self, listing: AuctionListing):
        self.auction_listings[listing.id] = listing

    def search_auction_listings(self, keyword: str) -> List[AuctionListing]:
        return [listing for listing in self.auction_listings.values() if keyword.lower() in listing.item_name.lower()]

    def place_bid(self, listing_id: str, bid: Bid):
        listing = self.auction_listings.get(listing_id)
        if listing:
            listing.place_bid(bid)


# -------------------------------
# Auction System Demo Class
# -------------------------------
class AuctionSystemDemo:
    @staticmethod
    def run():
        auction_system = AuctionSystem.get_instance()

        # Register users
        user1 = User("1", "John Doe", "john@example.com")
        user2 = User("2", "Jane Smith", "jane@example.com")
        auction_system.register_user(user1)
        auction_system.register_user(user2)

        # Create auction listings
        listing1 = AuctionListing("1", "Item 1", "Description 1", 100.0, 1, user1)
        listing2 = AuctionListing("2", "Item 2", "Description 2", 50.0, 1, user2)
        auction_system.create_auction_listing(listing1)
        auction_system.create_auction_listing(listing2)

        # Search auction listings
        search_results = auction_system.search_auction_listings("Item")
        print("Search Results:")
        for listing in search_results:
            print(listing.item_name)

        # Place bids
        bid1 = Bid("1", user2, 150.0)
        bid2 = Bid("2", user1, 200.0)
        auction_system.place_bid(listing1.id, bid1)
        auction_system.place_bid(listing1.id, bid2)


# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    AuctionSystemDemo.run()
