import datetime
import re
from position import Position
from payroll import Payroll

class Employee:
    def __init__(self, employee_id: str, first_name: str, last_name: str,
                 position: Position, hire_date: datetime.date,
                 email: str = None, phone: str = None):
        if not re.match(r'^[A-Za-zА-Яа-яЇїІіЄєҐґ\'\-]+$', first_name) or not re.match(r'^[A-Za-zА-Яа-яЇїІіЄєҐґ\'\-]+$', last_name):
            raise ValueError("Ім'я та прізвище повинні містити лише літери")
        if hire_date > datetime.date.today():
            raise ValueError("Дата прийняття не може бути в майбутньому")

        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.hire_date = hire_date
        self.email = email
        self.phone = phone
        self.payroll = Payroll(position.salary)

    def update_position(self, new_position: Position):
        self.position = new_position
        self.payroll.base_salary = new_position.salary

    def add_bonus(self, amount: float):
        self.payroll.add_bonus(amount)

    def get_full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def get_years_of_service(self) -> int:
        today = datetime.date.today()
        years = today.year - self.hire_date.year
        if (today.month, today.day) < (self.hire_date.month, self.hire_date.day):
            years -= 1
        return years

    def __str__(self):
        return f"ID: {self.employee_id}, ПІБ: {self.get_full_name()}, Посада: {self.position.title}, Стаж: {self.get_years_of_service()} років"