from abc import ABC, abstractmethod
from enum import Enum

class Pizza(ABC):
    @abstractmethod
    def get_cost(self):
        pass

class SIZE(Enum):
    SMALL = 1
    MEDIUM  = 1.5
    LARGE = 2

class Marg(Pizza):
    def __init__(self, size) -> None:
        self.cost = 10
        self.size = size

    def get_cost(self):
        return self.cost * self.size.value
    
class Pep(Pizza):
    def __init__(self, size):
        self.cost = 10
        self.size = size
    
    def get_cost(self):
        return self.cost * self.size.value

class Toppings(Pizza):
    def __init__(self, pizza) -> None:
        self.pizza = pizza

    def get_cost(self):
        pass

class Cheese(Toppings):
    def __init__(self, pizza) -> None:
        super().__init__(pizza)
    
    def get_cost(self):
        return self.pizza.get_cost() + 2 * self.pizza.size.value

class Mushroom(Toppings):
    def __init__(self, pizza) -> None:
        super().__init__(pizza)
    
    def get_cost(self):
        return self.pizza.get_cost() + 2 * self.pizza.size.value

p1 = Mushroom(Marg(SIZE.MEDIUM))
p2 = Cheese(Pep(SIZE.LARGE))
print(p1.get_cost())
print(p2.get_cost())