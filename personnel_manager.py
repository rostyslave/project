from typing import List, Dict, Optional
import csv
from employee import Employee
from position import Position

class PersonnelManager:
    def __init__(self):
        self.employees: List[Employee] = []
        self.positions: Dict[str, Position] = {}

    def add_position(self, position: Position) -> bool:
        if position.title not in self.positions:
            self.positions[position.title] = position
            return True
        return False

    def add_employee(self, employee: Employee) -> bool:
        if not any(emp.employee_id == employee.employee_id for emp in self.employees):
            self.employees.append(employee)
            return True
        return False

    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    def remove_employee(self, employee_id: str) -> bool:
        employee = self.get_employee_by_id(employee_id)
        if employee:
            self.employees.remove(employee)
            return True
        return False

    def update_employee(self, employee_id: str, **kwargs) -> bool:
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            return False

        for key, value in kwargs.items():
            if key == 'position' and isinstance(value, str) and value in self.positions:
                employee.update_position(self.positions[value])
            elif key in ['first_name', 'last_name', 'email', 'phone']:
                setattr(employee, key, value)
        return True

    def sort_employees(self, criteria: str = 'last_name') -> List[Employee]:
        if criteria == 'position':
            return sorted(self.employees, key=lambda emp: emp.position.title)
        elif criteria == 'hire_date':
            return sorted(self.employees, key=lambda emp: emp.hire_date)
        else:
            return sorted(self.employees, key=lambda emp: emp.get_full_name())

    def calculate_total_payroll(self) -> Dict[str, float]:
        total_gross = sum(emp.payroll.calculate_gross_salary() for emp in self.employees)
        total_tax = sum(emp.payroll.calculate_tax() for emp in self.employees)
        total_net = sum(emp.payroll.calculate_net_salary() for emp in self.employees)
        return {'total_gross': total_gross, 'total_tax': total_tax, 'total_net': total_net}

    def save_to_csv(self, filename: str = 'employees.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Прізвище', 'Ім\'я', 'Посада', 'Дата прийняття', 'Email', 'Телефон', 'Зарплата', 'Премія'])
            for employee in self.employees:
                writer.writerow([
                    employee.employee_id, employee.last_name, employee.first_name,
                    employee.position.title, employee.hire_date.strftime('%Y-%m-%d'),
                    employee.email or '', employee.phone or '',
                    employee.payroll.base_salary, employee.payroll.bonus
                ])