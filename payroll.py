class Payroll:
    TAX_RATE = 0.20

    def __init__(self, base_salary: float, bonus: float = 0):
        self.base_salary = base_salary
        self.bonus = bonus

    def calculate_gross_salary(self) -> float:
        return self.base_salary + self.bonus

    def calculate_tax(self) -> float:
        return self.calculate_gross_salary() * self.TAX_RATE

    def calculate_net_salary(self) -> float:
        return self.calculate_gross_salary() - self.calculate_tax()

    def add_bonus(self, amount: float):
        self.bonus += amount

    def __str__(self):
        return f"Загальна зарплата: {self.calculate_gross_salary()}, Податок: {self.calculate_tax()}, Чиста зарплата: {self.calculate_net_salary()}"