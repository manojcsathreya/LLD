import random
import threading

# Enum for defining the board positions (snake and ladder endpoints)
from enum import Enum


class OrderStatus(Enum):
    PENDING = 1
    PREPARING = 2
    READY = 3
    COMPLETED = 4
    CANCELLED = 5


class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2
    MOBILE_PAYMENT = 3


class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3


class VehicleType(Enum):
    CAR = 1
    MOTORCYCLE = 2
    TRUCK = 3


# Board-related classes (for the Snake and Ladder game)
class Snake:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class Ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position


class Board:
    BOARD_SIZE = 100

    def __init__(self):
        self.snakes = []
        self.ladders = []
        self._initialize_snakes_and_ladders()

    def _initialize_snakes_and_ladders(self):
        self.snakes.append(Snake(16, 6))
        self.snakes.append(Snake(48, 26))
        self.snakes.append(Snake(64, 60))
        self.snakes.append(Snake(93, 73))

        self.ladders.append(Ladder(1, 38))
        self.ladders.append(Ladder(4, 14))
        self.ladders.append(Ladder(9, 31))
        self.ladders.append(Ladder(21, 42))
        self.ladders.append(Ladder(28, 84))
        self.ladders.append(Ladder(51, 67))
        self.ladders.append(Ladder(80, 99))

    def get_board_size(self):
        return Board.BOARD_SIZE

    def get_new_position_after_snake_or_ladder(self, position):
        for snake in self.snakes:
            if snake.get_start() == position:
                return snake.get_end()

        for ladder in self.ladders:
            if ladder.get_start() == position:
                return ladder.get_end()

        return position


class Dice:
    MIN_VALUE = 1
    MAX_VALUE = 6

    def roll(self):
        return random.randint(Dice.MIN_VALUE, Dice.MAX_VALUE)


# Game Management classes
class GameManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.games = []

    @staticmethod
    def get_instance():
        if not GameManager._instance:
            with GameManager._lock:
                if not GameManager._instance:
                    GameManager._instance = GameManager()
        return GameManager._instance

    def start_new_game(self, player_names):
        game = SnakeAndLadderGame(player_names)
        self.games.append(game)
        threading.Thread(target=game.play).start()


# Game class to handle gameplay logic
class SnakeAndLadderGame:
    def __init__(self, player_names):
        self.board = Board()
        self.dice = Dice()
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0

    def play(self):
        while not self._is_game_over():
            current_player = self.players[self.current_player_index]
            dice_roll = self.dice.roll()
            new_position = current_player.get_position() + dice_roll

            if new_position <= self.board.get_board_size():
                current_player.set_position(self.board.get_new_position_after_snake_or_ladder(new_position))
                print(f"{current_player.get_name()} rolled a {dice_roll} and moved to position {current_player.get_position()}")

            if current_player.get_position() == self.board.get_board_size():
                print(f"{current_player.get_name()} wins!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _is_game_over(self):
        for player in self.players:
            if player.get_position() == self.board.get_board_size():
                return True
        return False


# Demo to showcase the functionality
class SnakeAndLadderDemo:
    @staticmethod
    def run():
        game_manager = GameManager.get_instance()

        # Start game 1
        players1 = ["Player 1", "Player 2", "Player 3"]
        game_manager.start_new_game(players1)

        # Start game 2
        players2 = ["Player 4", "Player 5"]
        game_manager.start_new_game(players2)


if __name__ == "__main__":
    SnakeAndLadderDemo.run()

