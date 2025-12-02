import re  # Імпортуємо модуль для регулярних виразів (для статичного методу)
from datetime import datetime


# --- Батьківські класи (для спадкування) ---
# Ми вигадаємо ці класи, як дозволено у пункті 2b, 
# оскільки Client і Courier мають спільні риси (ім'я, прізвище, телефон).

class Person:
    """
    Базовий клас "Людина".
    Використовується як спільний батьківський клас для Client та Courier.
    """

    def __init__(self, first_name: str, last_name: str, phone_num: str):
        self.first_name = first_name
        self.last_name = last_name
        self.__phone_num = phone_num  # Приватна властивість

    def get_full_name(self) -> str:
        """Повертає повне ім'я. Буде перевизначений (поліморфізм)."""
        return f"{self.first_name} {self.last_name}"

    def update_phone(self, new_phone: str):
        """Метод для оновлення приватного номера телефону."""
        print(f"Оновлення номера для {self.first_name}...")
        self.__phone_num = new_phone

    def get_phone(self) -> str:
        """Метод для читання приватного номера телефону."""
        return self.__phone_num


class Vehicle:
    """
    Другий батьківський клас для демонстрації множинного спадкування.
    Кур'єр (Courier) буде використовувати цей клас.
    """

    def __init__(self, vehicle_number: str, model: str):
        self.vehicle_number = vehicle_number
        self.model = model

    def get_vehicle_info(self) -> str:
        """Повертає інформацію про транспортний засіб."""
        return f"ТЗ: [{self.vehicle_number}] ({self.model})"


# -----------------------------------------------------------------
# ЧАСТИНА 1: Створення класу, що описує сутність з таблиці
# Ми об'єднаємо це з Частиною 2 і створимо дочірній клас Client.
# Він буде задовольняти всі вимоги Частини 1.
# -----------------------------------------------------------------

class Client(Person):
    """
    Клас Client (Клієнт), успадкований від Person.
    Цей клас виконує всі вимоги з ЧАСТИНИ 1.
    """

    # a. Конструктор (__init__)
    def __init__(self, client_id: int, first_name: str, last_name: str, phone_num: str):
        # Виклик конструктора батьківського класу
        super().__init__(first_name, last_name, phone_num)

        # d. Приватна властивість
        self.__client_id = client_id

        # b. Властивості (як мінімум 2)
        # (self.first_name і self.last_name успадковані)
        self.balance = 0.0  # Додамо власну властивість

    # c. Методи (як мінімум 2)
    def get_client_id(self) -> int:
        """Метод без параметрів (для читання приватного ID)."""
        return self.__client_id

    def add_to_balance(self, amount: float):
        """Метод з параметром."""
        if amount > 0:
            self.balance += amount
            print(f"Баланс клієнта {self.first_name} поповнено на {amount}. "
                  f"Новий баланс: {self.balance}")
        else:
            print("Сума поповнення має бути позитивною.")

    # e. Статичний метод
    @staticmethod
    def is_valid_client_id(client_id: int) -> bool:
        """
        Статичний метод для перевірки, чи є ID клієнта валідним (проста логіка).
        Він не прив'язаний до конкретного екземпляру (self).
        """
        print(f"(Static check) Перевірка ID: {client_id}...")
        return client_id > 0

    # Демонстрація Поліморфізму:
    # Ми перевизначаємо метод get_full_name() з батьківського класу Person
    def get_full_name(self) -> str:
        """Повертає повне ім'я з префіксом 'Клієнт'."""
        return f"[КЛІЄНТ] {self.first_name} {self.last_name}"


# -----------------------------------------------------------------
# ЧАСТИНА 2: Створення дочірніх класів
# -----------------------------------------------------------------

# Перший дочірній клас - Client (створений вище).

# a. Другий дочірній клас з множинним наслідуванням
class Courier(Person, Vehicle):
    """
    Клас Courier (Кур'єр).
    Демонструє множинне спадкування:
    - Успадковує дані про особу від Person (ім'я, телефон).
    - Успадковує дані про авто від Vehicle (номер, модель).
    """

    def __init__(self, courier_id: int, first_name: str, last_name: str,
                 phone_num: str, vehicle_number: str, model: str):
        # Виклик конструкторів обох батьківських класів
        Person.__init__(self, first_name, last_name, phone_num)
        Vehicle.__init__(self, vehicle_number, model)

        self.courier_id = courier_id

    # Демонстрація Поліморфізму:
    # Знову перевизначаємо той самий метод
    def get_full_name(self) -> str:
        """Повертає повне ім'я з префіксом 'Кур'єр'."""
        return f"[КУР'ЄР] {self.first_name} {self.last_name}"

    def assign_delivery(self, shipment_id: int):
        """Власний метод кур'єра."""
        print(f"Кур'єр {self.first_name} взяв в роботу відправлення #{shipment_id}")


# --- Додатковий клас для демонстрації згідно схеми ERD ---

class Shipment:
    """
    Клас Shipment (Відправлення). 
    Він буде використовувати екземпляри Client і Courier (композиція),
    щоб продемонструвати доменний метод.
    """

    def __init__(self, shipment_id: int, client: Client, courier: Courier,
                 description: str, price: float):
        self.shipment_id = shipment_id
        self.client = client  # Екземпляр класу Client
        self.courier = courier  # Екземпляр класу Courier
        self.description = description
        self.price = price
        self.status = "Очікує"
        self.when_created = datetime.now()

    # c. Базовий метод роботи з предметною областю (вибити чек)
    def print_receipt(self):
        """
        Демонстрація доменного методу "вибити чек".
        Цей метод демонструє поліморфізм в дії,
        використовуючи self.client.get_full_name() та self.courier.get_full_name().
        """
        print("=" * 30)
        print(f"КВИТАНЦІЯ НА ВІДПРАВЛЕННЯ #{self.shipment_id}")
        print(f"Дата: {self.when_created.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 30)

        # --- ПОЛІМОРФІЗМ ТУТ ---
        # Викликається той самий метод get_full_name(), 
        # але він дає різний результат для Client і Courier.
        print(f"Відправник: {self.client.get_full_name()}")
        print(f"Виконавець: {self.courier.get_full_name()}")
        # ---

        print(f"Інфо про авто: {self.courier.get_vehicle_info()}")
        print(f"Опис: {self.description}")
        print("-" * 30)
        print(f"Загальна вартість: {self.price} грн")
        print("=" * 30)


# -----------------------------------------------------------------
# ЧАСТИНА 3: Демонстраційний алгоритм
# -----------------------------------------------------------------

print("--- Початок демонстрації ---")

# a. Створення екземплярів дочірніх класів
print("\n--- a. Створення екземплярів ---")
client1 = Client(
    client_id=101,
    first_name="Іван",
    last_name="Франко",
    phone_num="0991112233"
)

courier1 = Courier(
    courier_id=55,
    first_name="Василь",
    last_name="Стефаник",
    phone_num="0678889900",
    vehicle_number="BC1234AA",
    model="Ford Transit"
)

print(f"Створено: {client1.get_full_name()}")
print(f"Створено: {courier1.get_full_name()}")

# b. Виклик методів і робота з властивостями
print("\n--- b. Робота з методами та властивостями ---")

# Робота з Client
client1.add_to_balance(500.0)
print(f"Баланс клієнта: {client1.balance}")

# Виклик статичного методу (зверніть увагу - він викликається від Класу, а не екземпляру)
print(f"Чи є ID 101 валідним? {Client.is_valid_client_id(101)}")
print(f"Чи є ID -5 валідним? {Client.is_valid_client_id(-5)}")

# Робота з Courier
print(f"Телефон кур'єра: {courier1.get_phone()}")
print(f"Авто кур'єра: {courier1.get_vehicle_info()}")  # Метод з Vehicle
courier1.assign_delivery(shipment_id=12345)

# Демонстрація Поліморфізму
print("\n--- b. Демонстрація Поліморфізму ---")
# Створимо список, що містить об'єкти різних класів,
# але зі спільним предком (Person)
people_list = [client1, courier1]

for person in people_list:
    # Викликаємо ОДИН і ТОЙ САМИЙ метод get_full_name(),
    # але отримуємо РІЗНУ поведінку залежно від реального класу об'єкта.
    print(f"Об'єкт {person.__class__.__name__} каже: {person.get_full_name()}")

# c. Використання базових методів предметної області
print("\n--- c. Доменний метод (вибити чек) ---")

# Створимо екземпляр Shipment, передавши йому клієнта і кур'єра
shipment1 = Shipment(
    shipment_id=12345,
    client=client1,
    courier=courier1,
    description="Документи та книги",
    price=150.0
)

# Викличемо доменний метод "вибити чек"
# Цей метод сам використовує поліморфізм (див. його реалізацію вище)
shipment1.print_receipt()

print("\n--- Кінець демонстрації ---")