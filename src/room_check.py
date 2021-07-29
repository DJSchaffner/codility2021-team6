from dataclasses import dataclass

import itertools as it

from datetime import datetime

from api_access import query_live_data


@dataclass
class Room:
    id: str
    powerConsumption: float
    temperature: float
    sensors: dict
    workplaceReservations: int

    def _check_light(self, end_time: int) -> (bool, list):
        dt = datetime.fromtimestamp(end_time)

        # Those hours should have sun outside all year
        if dt > 8 and dt < 17 and self.sensors['lightOn'] and self.sensors['rollerBlindsClosed']:
            return False, ["Licht ist an und Rolläden sind unten"]
        else:
            return True, []

    def _check_heater(self) -> (bool, list):
        if not self.sensors['heaterRunning']:
            return True, []
        if self.sensors['windowsOpen']:
            return False, ["Fenster ist offen, während die Heizung läuft"]
        if self.sensors['airConditioningRunning']:
            return False, ["Klimaanlage und Heizung laufen beide"]
        return True, []

    def _check_aircon(self) -> (bool, list):
        if not self.sensors['airConditioningRunning']:
            return True, []
        if self.sensors['windowsOpen']:
            return False, ["Fenster ist offen, während die Klimaanlage läuft"]
        if self.sensors['airConditioningRunning']:
            return False, ["Klimaanlage und Heizung laufen beide"]
        return True, []

    def _check_room_free(self, end_time: int, num_employees_total: int) -> (bool, list):
        problems = []
        if num_employees_total > 0 and self.workplaceReservations > 0:
            return True, []
        if self.sensors['lightOn']:
            problems.append("Raum ist leer, aber Licht ist an")
        if self.sensors['windowsOpen']:
            problems.append("Raum ist leer, aber Fenster ist offen")
        if self.sensors['airConditioningRunning']:
            problems.append("Raum ist leer, aber Klimaanlage läuft")
        if self.sensors['heaterRunning']:
            if self.temperature > 18:
                problems.append(
                    "Raum ist leer, aber wird auf über 18° Celsius geheizt")
            else:
                dt = datetime.fromtimestamp(end_time)
                if (dt.hour >= 22 or dt.hour < 6) and self.temperature > 6:
                    problems.append(
                        "Raum ist leer und wird nachts auf "
                        "über 6° Celsius geheizt")
        return len(problems) == 0, problems

    def check_sensors(self, end_time: int, num_employees_total: int) -> (bool, list):
        heater = self._check_heater()
        ac = self._check_aircon()
        free = self._check_room_free(end_time, num_employees_total)
        if heater[0] and ac[0] and free[0]:
            return True, []
        else:
            problems = [heater[1], ac[1], free[1]]
            problems = list(it.chain(*problems))
            return False, ', '.join(list(dict.fromkeys(problems)))


def live_room_check():
    status = []
    json = query_live_data()
    rooms_json = json["rooms"]
    end_time = json["samplingStopTime"]
    num_employees_total = json["building"]["totalEmployeesIn"]
    for r in rooms_json:
        room = Room(**r)
        check = room.check_sensors(end_time, num_employees_total)
        if not check[0]:
            status.append(
                {'Raum': room.id, 'In Ordnung': False, 'Problem(e)': check[1]})
        else:
            status.append(
                {'Raum': room.id, 'In Ordnung': True, 'Problem(e)': "-"})
    return status
