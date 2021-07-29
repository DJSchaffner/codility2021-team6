from dataclasses import dataclass

from api_access import query_live_data


@dataclass
class Room:
    id: str
    powerConsumption: float
    temperature: float
    sensors: dict
    workplaceReservations: int

    def _check_heater(self) -> (bool, str):
        if not self.sensors['heaterRunning']:
            return True, ""
        if self.sensors['windowsOpen']:
            return False, "Heater is running while window is open"
        if self.sensors['airConditioningRunning']:
            return False, "Heater and air conditioning running at the same time"
        return True, ""

    def _check_aircon(self) -> (bool, str):
        if not self.sensors['airConditioningRunning']:
            return True, ""
        if self.sensors['windowsOpen']:
            return False, "Air conditioning is running while window is open"
        if self.sensors['airConditioningRunning']:
            return False, "Heater and air conditioning running at the same time"
        return True, ""

    def check_sensors(self) -> (bool, list):
        heater = self._check_heater()
        ac = self._check_aircon()
        if heater[0] and ac[0]:
            return True, []
        else:
            problems = [heater[1], ac[1]]
            problems = [p for p in problems if p != ""]
            return False, list(dict.fromkeys(problems))


def live_room_check():
    problems = []
    json = query_live_data()
    rooms_json = json["rooms"]
    for r in rooms_json:
        room = Room(**r)
        check = room.check_sensors()
        if not check[0]:
            problems.append((room.id, check[1]))
    return problems
