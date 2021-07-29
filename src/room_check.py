from dataclasses import dataclass


@dataclass
class Room:
    id: str
    powerConsumption: float
    temperature: float
    sensors: dict
    workplaceReservations: int

    def check_heater(self) -> (bool, str):
        if not self.sensors['heaterRunning']:
            return True, ""
        if self.sensors['windowsOpen']:
            return False, "Heater is running while window is open"
        if self.sensors['airConditioningRunning']:
            return False, "Heater and air conditioning running at the same time"
