import datetime
import re
from typing import List, Dict, Optional

class Position:
    ALLOWED_ACCESS_LEVELS = [1, 2, 3, 4, 5]

    def __init__(self, title: str, salary: float, access_level: int):
        self.title = title
        self.salary = salary
        if access_level in self.ALLOWED_ACCESS_LEVELS:
            self.access_level = access_level
        else:
            raise ValueError(f"Неправильний рівень доступу. Дозволені рівні: {self.ALLOWED_ACCESS_LEVELS}")

    def __str__(self):
        return f"Посада: {self.title}, Зарплата: {self.salary}, Рівень доступу: {self.access_level}"
