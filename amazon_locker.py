import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    EXTRALARGE = 4


class Status(Enum):
    FREE = 1
    OCCUPIED = 2
    RESERVED = 3

class IItem(ABC):
    @abstractmethod
    def get_size(self) -> Size:
        pass

class Item(IItem):
    def __init__(self, size: Size):
        self.size = size

    def get_size(self) -> Size:
        return self.size

# Locker
class ILocker(ABC):
    @abstractmethod
    def update_status(self, status: Status) -> None:
        pass

    @abstractmethod
    def get_size(self) -> Size:
        pass

    @abstractmethod
    def get_status(self) -> Status:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass


class Locker(ILocker):
    def __init__(self, locker_id: int, size: Size, status: Status = Status.FREE):
        self.id = locker_id
        self.size = size
        self.status = status

    def update_status(self, status: Status) -> None:
        self.status = status

    def get_size(self) -> Size:
        return self.size

    def get_status(self) -> Status:
        return self.status

    def get_id(self) -> int:
        return self.id


# Locker System Interface and Implementation

class ILockerSystem(ABC):
    @abstractmethod
    def find_locker_for_item(self, item: IItem) -> Optional[ILocker]:
        pass

    @abstractmethod
    def add_item(self, item: IItem, locker: ILocker, code: str) -> bool:
        pass

    @abstractmethod
    def remove_item(self, locker: ILocker, code: str) -> Optional[IItem]:
        pass

    @abstractmethod
    def generate_code(self, locker: ILocker) -> str:
        pass


class LockerSystem(ILockerSystem):
    def __init__(self):
        self.lockers_size_status_map: Dict[Size, Dict[Status, Dict[int, Locker]]] = {
            sz: {st: {} for st in Status} for sz in Size
        }
        self.code_locker_map: Dict[str, Locker] = {}
        self.locker_item_map: Dict[int, IItem] = {}

    def find_locker_for_item(self, item: IItem) -> Optional[ILocker]:
        item_size = item.get_size()
        for size in Size:
            if size.value >= item_size.value:
                available_lockers = self.lockers_size_status_map.get(size, {}).get(Status.FREE, {})
                if available_lockers:
                    locker = next(iter(available_lockers.values()))
                    locker.update_status(Status.RESERVED)
                    # Update the status maps
                    self.lockers_size_status_map[size][Status.FREE].pop(locker.get_id(), None)
                    self.lockers_size_status_map[size][Status.RESERVED][locker.get_id()] = locker
                    return locker
        return None

    def add_item(self, item: IItem, locker: ILocker, code: str) -> bool:
        if code in self.code_locker_map and self.code_locker_map[code].get_id() == locker.get_id():
            locker.update_status(Status.OCCUPIED)
            self.locker_item_map[locker.get_id()] = item
            # Update status maps
            self.lockers_size_status_map[locker.get_size()][Status.RESERVED].pop(locker.get_id(), None)
            self.lockers_size_status_map[locker.get_size()][Status.OCCUPIED][locker.get_id()] = locker
            # Remove the code from the map since it's used
            del self.code_locker_map[code]
            return True
        return False

    def remove_item(self, locker: ILocker, code: str) -> Optional[IItem]:
        if code in self.code_locker_map and self.code_locker_map[code].get_id() == locker.get_id():
            item = self.locker_item_map.pop(locker.get_id(), None)
            locker.update_status(Status.FREE)
            # Update status maps
            self.lockers_size_status_map[locker.get_size()][Status.OCCUPIED].pop(locker.get_id(), None)
            self.lockers_size_status_map[locker.get_size()][Status.FREE][locker.get_id()] = locker
            # Remove the code from the map since it's used
            del self.code_locker_map[code]
            return item
        return None

    def generate_code(self, locker: ILocker) -> str:
        code = str(uuid.uuid4())
        self.code_locker_map[code] = locker
        return code


# Agent Interface and Implementation

class IAgent(ABC):
    @abstractmethod
    def execute_delivery(self, item: IItem, locker: ILocker, user: 'IUser') -> bool:
        pass


class Agent(IAgent):
    def __init__(self, locker_system: ILockerSystem):
        self.locker_system = locker_system
        self.master_code = str(uuid.uuid4())

    def execute_delivery(self, item: IItem, locker: ILocker, user: 'IUser') -> bool:
        if self.locker_system.add_item(item, locker, self.master_code):
            code = self.locker_system.generate_code(locker)
            # Simulate sending the code to the user
            print(f"Code {code} sent to user.")
            return True
        return False


# User Interface and Implementation

class IUser(ABC):
    @abstractmethod
    def opt_for_locker_delivery(self, item: IItem) -> Optional[ILocker]:
        pass

    @abstractmethod
    def get_item_from_locker(self, code: str, locker: ILocker) -> Optional[IItem]:
        pass

    @abstractmethod
    def opt_for_locker_return(self, item: IItem) -> Optional[ILocker]:
        pass

    @abstractmethod
    def return_item_to_locker(self, item: IItem, code: str, locker: ILocker) -> bool:
        pass


class User(IUser):
    def __init__(self, mobile: str, locker_system: ILockerSystem):
        self.mobile = mobile
        self.locker_system = locker_system

    def opt_for_locker_delivery(self, item: IItem) -> Optional[ILocker]:
        locker = self.locker_system.find_locker_for_item(item)
        if locker:
            print(f"Locker {locker.get_id()} reserved for delivery.")
        return locker

    def get_item_from_locker(self, code: str, locker: ILocker) -> Optional[IItem]:
        return self.locker_system.remove_item(locker, code)

    def opt_for_locker_return(self, item: IItem) -> Optional[ILocker]:
        locker = self.locker_system.find_locker_for_item(item)
        if locker:
            code = self.locker_system.generate_code(locker)
            print(f"Return code {code} sent to user.")
        return locker

    def return_item_to_locker(self, item: IItem, code: str, locker: ILocker) -> bool:
        return self.locker_system.add_item(item, locker, code)


def main():
    # Initialize lockers with different sizes and statuses
    lockers = [
        Locker(locker_id=1, size=Size.SMALL),
        Locker(locker_id=2, size=Size.MEDIUM),
        Locker(locker_id=3, size=Size.LARGE),
        Locker(locker_id=4, size=Size.EXTRALARGE)
    ]

    # Initialize LockerSystem with the created lockers
    locker_system = LockerSystem()
    for locker in lockers:
        locker_system.lockers_size_status_map[locker.get_size()][locker.get_status()][locker.get_id()] = locker

    # Create an agent with the locker system
    agent = Agent(locker_system)

    # User who interacts with the locker system
    user = User(mobile="123-456-7890", locker_system=locker_system)

    # Simulate adding an item for locker delivery
    small_item = Item(size=Size.SMALL)
    print("\nUser requests locker delivery for a small item:")
    delivery_locker = user.opt_for_locker_delivery(small_item)
    if delivery_locker:
        # Agent completes the delivery
        if agent.execute_delivery(small_item, delivery_locker, user):
            print(f"Delivery completed and code sent to user for locker {delivery_locker.get_id()}.")

    # Simulate user retrieving item from the locker using the code
    retrieval_code = locker_system.generate_code(delivery_locker)  # Simulate code generated during delivery
    print("\nUser retrieves item from locker using the code:")
    retrieved_item = user.get_item_from_locker(retrieval_code, delivery_locker)
    if retrieved_item:
        print(f"Item successfully retrieved from locker {delivery_locker.get_id()}.")

    # Simulate user returning an item to a locker
    print("\nUser requests locker return for the item:")
    return_locker = user.opt_for_locker_return(small_item)
    if return_locker:
        return_code = locker_system.generate_code(return_locker)
        print(f"Return code {return_code} sent to user.")
        # User returns the item to the locker
        if user.return_item_to_locker(small_item, return_code, return_locker):
            print(f"Item successfully returned to locker {return_locker.get_id()}.")


# Run the main function
if __name__ == "__main__":
    main()
