from enum import Enum


class DriverOrderField(str, Enum):
    NAME = "name"
    DATE_OF_BIRTH = "date_of_birth"
    TOTAL_CHAMPIONSHIP_WINS = "total_championship_wins"
    TOTAL_CHAMPIONSHIP_POINTS = "total_championship_points"
    TOTAL_RACE_WINS = "total_race_wins"
    TOTAL_PODIUMS = "total_podiums"
    TOTAL_POINTS = "total_points"
    TOTAL_POLE_POSITIONS = "total_pole_positions"
    TOTAL_FASTEST_LAPS = "total_fastest_laps"
