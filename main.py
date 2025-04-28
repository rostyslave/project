import datetime
from position import Position
from employee import Employee
from personnel_manager import PersonnelManager


def main():
    manager = PersonnelManager()

    for pos in [Position("Директор", 50000, 5), Position("Менеджер", 30000, 3), Position("Розробник", 40000, 2)]:
        manager.add_position(pos)

    emp1 = Employee("E001", "Іван", "Петренко", manager.positions["Директор"],
                    datetime.date(2015, 5, 10), "ivan@example.com", "+380501234567")
    emp1.add_bonus(5000)
    manager.add_employee(emp1)
    manager.add_employee(Employee("E002", "Марія", "Ковальчук", manager.positions["Менеджер"],
                                  datetime.date(2018, 3, 15), "maria@example.com", "+380672345678"))

    while True:
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛІННЯ ПЕРСОНАЛОМ".center(50, " "))
        print("=" * 50)
        print("1. Перегляд списку співробітників")
        print("2. Додавання нового співробітника")
        print("3. Видалення співробітника")
        print("4. Оновлення інформації про співробітника")
        print("5. Перегляд фінансових показників")
        print("0. Вихід")
        print("=" * 50)

        choice = input("\nВиберіть опцію: ")

        if choice == '0':
            print("Дякуємо за використання системи!")
            break

        elif choice == '1':
            criteria = 'last_name'
            sort_choice = input("Сортувати за: 1-Прізвищем, 2-Посадою, 3-Датою прийняття: ")
            if sort_choice == '2':
                criteria = 'position'
            elif sort_choice == '3':
                criteria = 'hire_date'

            print("\n" + "=" * 50)
            print("СПИСОК СПІВРОБІТНИКІВ".center(50, " "))
            print("=" * 50)
            for emp in manager.sort_employees(criteria):
                print(emp)
            print("=" * 50)

        elif choice == '2':
            print("\n" + "=" * 50)
            print("ДОДАВАННЯ НОВОГО СПІВРОБІТНИКА".center(50, " "))
            print("=" * 50)
            if not manager.positions:
                print("Немає доступних посад!")
                continue

            employee_id = input("ID співробітника: ")
            if any(emp.employee_id == employee_id for emp in manager.employees):
                print(f"Співробітник з ID {employee_id} вже існує!")
                continue

            try:
                first_name = input("Ім'я: ")
                last_name = input("Прізвище: ")

                print("\n" + "=" * 50)
                print("ДОСТУПНІ ПОСАДИ".center(50, " "))
                print("=" * 50)
                pos_titles = list(manager.positions.keys())
                for i, title in enumerate(pos_titles, 1):
                    print(f"{i}. {title} (Зарплата: {manager.positions[title].salary})")
                print("=" * 50)

                pos_idx = int(input("Виберіть номер посади: ")) - 1
                if pos_idx < 0 or pos_idx >= len(pos_titles):
                    print("Невірний номер посади!")
                    continue

                hire_date = datetime.datetime.strptime(input("Дата прийняття (РРРР-ММ-ДД): "), '%Y-%m-%d').date()
                email = input("Email (необов'язково): ") or None
                phone = input("Телефон (необов'язково): ") or None

                new_emp = Employee(employee_id, first_name, last_name,
                                   manager.positions[pos_titles[pos_idx]], hire_date, email, phone)

                if manager.add_employee(new_emp):
                    print(f"Співробітник {new_emp.get_full_name()} успішно доданий!")
            except (ValueError, IndexError) as e:
                print(f"Помилка: {e}")

        elif choice == '3':
            print("\n" + "=" * 50)
            print("ВИДАЛЕННЯ СПІВРОБІТНИКА".center(50, " "))
            print("=" * 50)
            for emp in manager.employees:
                print(f"{emp.employee_id}: {emp.get_full_name()}")
            print("=" * 50)

            emp_id = input("ID співробітника для видалення: ")
            if manager.remove_employee(emp_id):
                print(f"Співробітник з ID {emp_id} видалений!")
            else:
                print(f"Співробітник з ID {emp_id} не знайдений!")

        elif choice == '4':
            print("\n" + "=" * 50)
            print("ОНОВЛЕННЯ ІНФОРМАЦІЇ".center(50, " "))
            print("=" * 50)
            for emp in manager.employees:
                print(f"{emp.employee_id}: {emp.get_full_name()}")
            print("=" * 50)

            emp_id = input("ID співробітника для оновлення: ")
            emp = manager.get_employee_by_id(emp_id)
            if not emp:
                print(f"Співробітник з ID {emp_id} не знайдений!")
                continue

            print(f"Обраний співробітник: {emp}")
            update_choice = input("Що оновити? 1-Ім'я, 2-Прізвище, 3-Посада, 4-Email, 5-Телефон, 6-Премія: ")

            try:
                if update_choice == '1':
                    manager.update_employee(emp_id, first_name=input("Нове ім'я: "))
                elif update_choice == '2':
                    manager.update_employee(emp_id, last_name=input("Нове прізвище: "))
                elif update_choice == '3':
                    print("\n" + "=" * 50)
                    print("ДОСТУПНІ ПОСАДИ".center(50, " "))
                    print("=" * 50)
                    pos_titles = list(manager.positions.keys())
                    for i, title in enumerate(pos_titles, 1):
                        print(f"{i}. {title}")
                    print("=" * 50)
                    pos_idx = int(input("Номер нової посади: ")) - 1
                    if 0 <= pos_idx < len(pos_titles):
                        manager.update_employee(emp_id, position=pos_titles[pos_idx])
                elif update_choice == '4':
                    manager.update_employee(emp_id, email=input("Новий email: "))
                elif update_choice == '5':
                    manager.update_employee(emp_id, phone=input("Новий телефон: "))
                elif update_choice == '6':
                    emp.add_bonus(float(input("Сума премії: ")))
                    print("Премію додано!")
            except (ValueError, IndexError) as e:
                print(f"Помилка: {e}")

        elif choice == '5':
            financials = manager.calculate_total_payroll()
            print("\n" + "=" * 50)
            print("ФІНАНСОВІ ПОКАЗНИКИ".center(50, " "))
            print("=" * 50)
            print(f"Загальна сума зарплат: {financials['total_gross']}")
            print(f"Загальна сума податків: {financials['total_tax']}")
            print(f"Чиста сума до виплати: {financials['total_net']}")
            print("=" * 50)

        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
