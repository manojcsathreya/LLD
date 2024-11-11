from enum import Enum
import threading
import time


class Signal(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3


class Road:
    def __init__(self, road_id, name):
        self.id = road_id
        self.name = name
        self.traffic_light = None

    def set_traffic_light(self, traffic_light):
        self.traffic_light = traffic_light

    def get_traffic_light(self):
        return self.traffic_light

    def get_id(self):
        return self.id


class TrafficLight:
    def __init__(self, id: str, red_duration: int, yellow_duration: int, green_duration: int):
        self.id = id
        self.current_signal = Signal.RED
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.lock = threading.Lock()

    def change_signal(self, new_signal: Signal):
        with self.lock:
            self.current_signal = new_signal
            self.notify_observers()

    def get_current_signal(self):
        return self.current_signal

    def notify_observers(self):
        print(f"Traffic light {self.id} changed to {self.current_signal.name}")


class TrafficController:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.roads = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def add_road(self, road: Road):
        self.roads[road.id] = road

    def remove_road(self, road_id: str):
        self.roads.pop(road_id, None)

    def start_traffic_control(self):
        for road in self.roads.values():
            traffic_light = road.get_traffic_light()
            threading.Thread(target=self._control_traffic_light, args=(traffic_light,), daemon=True).start()

    def _control_traffic_light(self, traffic_light: TrafficLight):
        while True:
            try:
                time.sleep(traffic_light.red_duration / 1000)  # Convert ms to seconds
                traffic_light.change_signal(Signal.GREEN)
                time.sleep(traffic_light.green_duration / 1000)
                traffic_light.change_signal(Signal.YELLOW)
                time.sleep(traffic_light.yellow_duration / 1000)
                traffic_light.change_signal(Signal.RED)
            except Exception as e:
                print(f"Error in traffic light control: {e}")

    def handle_emergency(self, road_id: str):
        road = self.roads.get(road_id)
        if road:
            traffic_light = road.get_traffic_light()
            traffic_light.change_signal(Signal.GREEN)
            print(f"Emergency handled: {road.name} traffic light set to GREEN")


class TrafficSignalSystemDemo:
    @staticmethod
    def run():
        traffic_controller = TrafficController.get_instance()

        # Create roads
        road1 = Road("R1", "Main Street")
        road2 = Road("R2", "Broadway")
        road3 = Road("R3", "Park Avenue")
        road4 = Road("R4", "Elm Street")

        # Create traffic lights with durations in milliseconds
        traffic_light1 = TrafficLight("TL1", 30000, 5000, 60000)
        traffic_light2 = TrafficLight("TL2", 30000, 5000, 60000)
        traffic_light3 = TrafficLight("TL3", 30000, 5000, 60000)
        traffic_light4 = TrafficLight("TL4", 30000, 5000, 60000)

        # Assign traffic lights to roads
        road1.set_traffic_light(traffic_light1)
        road2.set_traffic_light(traffic_light2)
        road3.set_traffic_light(traffic_light3)
        road4.set_traffic_light(traffic_light4)

        # Add roads to the traffic controller
        traffic_controller.add_road(road1)
        traffic_controller.add_road(road2)
        traffic_controller.add_road(road3)
        traffic_controller.add_road(road4)

        # Start traffic control
        traffic_controller.start_traffic_control()

        # Simulate an emergency on a specific road
        traffic_controller.handle_emergency("R2")


if __name__ == "__main__":
    TrafficSignalSystemDemo.run()
