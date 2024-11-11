from abc import ABC
from enum import Enum
from typing import List

# Enum for Vehicle Types
class VehicleType(Enum):
    CAR = 1
    MOTORCYCLE = 2
    TRUCK = 3

# Vehicle base class
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

    def get_type(self) -> VehicleType:
        return self.type


# Car class inheriting from Vehicle
class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)


# Motorcycle class inheriting from Vehicle
class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)


# Truck class inheriting from Vehicle
class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)


# Parking Spot class
class ParkingSpot:
    def __init__(self, spot_number: int):
        self.spot_number = spot_number
        self.vehicle_type = VehicleType.CAR  # Default vehicle type is CAR
        self.parked_vehicle = None

    def is_available(self) -> bool:
        return self.parked_vehicle is None

    def park_vehicle(self, vehicle: Vehicle) -> None:
        if self.is_available() and vehicle.get_type() == self.vehicle_type:
            self.parked_vehicle = vehicle
        else:
            raise ValueError("Invalid vehicle type or spot already occupied.")

    def unpark_vehicle(self) -> None:
        self.parked_vehicle = None

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type

    def get_parked_vehicle(self) -> Vehicle:
        return self.parked_vehicle

    def get_spot_number(self) -> int:
        return self.spot_number


# Level class representing a parking level in the parking lot
class Level:
    def __init__(self, floor: int, num_spots: int):
        self.floor = floor
        self.parking_spots: List[ParkingSpot] = [ParkingSpot(i) for i in range(num_spots)]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if spot.is_available() and spot.get_vehicle_type() == vehicle.get_type():
                spot.park_vehicle(vehicle)
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                return True
        return False

    def display_availability(self) -> None:
        print(f"Level {self.floor} Availability:")
        for spot in self.parking_spots:
            print(f"Spot {spot.get_spot_number()}: {'Available' if spot.is_available() else 'Occupied'}")


# Parking Lot class implementing Singleton pattern
class ParkingLot:
    _instance = None

    def __init__(self):
        if ParkingLot._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ParkingLot._instance = self
            self.levels: List[Level] = []

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            ParkingLot()
        return ParkingLot._instance

    def add_level(self, level: Level) -> None:
        self.levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.park_vehicle(vehicle):
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.unpark_vehicle(vehicle):
                return True
        return False

    def display_availability(self) -> None:
        for level in self.levels:
            level.display_availability()


# ParkingLotDemo class to demonstrate the working of the parking lot system
class ParkingLotDemo:
    @staticmethod
    def run():
        parking_lot = ParkingLot.get_instance()
        parking_lot.add_level(Level(1, 100))  # Adding level 1 with 100 spots
        parking_lot.add_level(Level(2, 80))   # Adding level 2 with 80 spots

        # Creating vehicles
        car = Car("ABC123")
        truck = Truck("XYZ789")
        motorcycle = Motorcycle("M1234")

        # Park vehicles
        parking_lot.park_vehicle(car)
        parking_lot.park_vehicle(truck)
        parking_lot.park_vehicle(motorcycle)

        # Display availability of parking spots
        parking_lot.display_availability()

        # Unpark vehicle (motorcycle)
        parking_lot.unpark_vehicle(motorcycle)

        # Display updated availability
        parking_lot.display_availability()


if __name__ == "__main__":
    ParkingLotDemo.run()