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
        """
        Checks whether the lights in the building are running in daylight when
        roller blinds are down
        :param end_time: the end timestamp of the observed interval
        :return: (True, []) if no problems with lighting were found,
        (False, [list with problems]) otherwise
        """
        dt = datetime.fromtimestamp(end_time).hour

        # Those hours should have sun outside all year
        if 8 < dt < 17 and self.sensors['lightOn'] and \
                self.sensors['rollerBlindsClosed']:
            return False, ["Licht ist an und Rollläden sind unten"]
        else:
            return True, []

    def _check_heater(self) -> (bool, list):
        """
        Checks whether heaters are running in rooms with open windows or
        running air cons
        :return: (True, []) if no problems with the heating were found,
        (False, [list with problems]) otherwise
        """
        if not self.sensors['heaterRunning']:
            return True, []
        if self.sensors['windowsOpen']:
            return False, ["Fenster ist offen, während die Heizung läuft"]
        if self.sensors['airConditioningRunning']:
            return False, ["Klimaanlage und Heizung laufen beide"]
        return True, []

    def _check_aircon(self) -> (bool, list):
        """
        Checks whether air cons are running in rooms with open windows or
        running heaters
        :return: (True, []) if no problems with air cons were found,
        (False, [list with problems]) otherwise
        """
        if not self.sensors['airConditioningRunning']:
            return True, []
        if self.sensors['windowsOpen']:
            return False, ["Fenster ist offen, während die Klimaanlage läuft"]
        if self.sensors['airConditioningRunning']:
            return False, ["Klimaanlage und Heizung laufen beide"]
        return True, []

    def _check_room_free(self, end_time: int, num_employees_total: int) \
            -> (bool, list):
        """
        Checks whether empty rooms are unnecessarily heated, have lights or
        air cons running or have open windows
        :param end_time: the end timestamp of the observed interval
        :param num_employees_total: the number of employees in the building
        :return: (True, []) if no problems with empty rooms were found,
        (False, [list with problems]) otherwise
        """
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

    def check_sensors(self, end_time: int, num_employees_total: int) \
            -> (bool, list):
        """
        Checks the sensors of a room for problems
        :param end_time: the end timestamp of the observed interval
        :param num_employees_total: the number of employees in the building
        :return: (True, []) if no problems were found for the room,
        (False, [list with problems]) otherwise
        """
        heater = self._check_heater()
        ac = self._check_aircon()
        free = self._check_room_free(end_time, num_employees_total)
        light = self._check_light(end_time)
        if heater[0] and ac[0] and free[0] and light[0]:
            return True, []
        else:
            problems = [heater[1], ac[1], free[1], light[1]]
            problems = list(it.chain(*problems))
            return False, ', '.join(list(dict.fromkeys(problems)))


def live_room_check():
    """
    Checks all rooms in the building for currently occurring problems
    :return: the list of rooms with a dict containing for each room whether and
    which problems occur
    """
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
