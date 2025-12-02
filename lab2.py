class Person:
    def __init__(self, firstname: str, lastname: str, phone_num: str):
        self.firstname = firstname
        self.lastname = lastname
        self.__phone_num = phone_num

    def getfullname(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def upd_phone_num(self, new_phone_num):
        print(f"Змінюємо номер для користувача: {self.getfullname()}")
        self.__phone_num = new_phone_num
        print("Номер змінено успішно")

    def getphone_num(self) -> str:
        return self.__phone_num


class Vehicle:
    def __init__(self, vehicle_num: str, model: str):
        self.vehicle_num = vehicle_num
        self.model = model


class Courier(Person, Vehicle):
    def __init__(self, courier_id: int, first_name: str, last_name: str, phone_num: str, vehicle_number: str = None,
                 model: str = None):
        Person.__init__(self, first_name, last_name, phone_num)

        if vehicle_number is not None:
            print(f"-> Кур'єру призначено транспорт.")
            Vehicle.__init__(self, vehicle_number, model)
        else:
            print(f"-> Кур'єр піший/на велосипеді.")
            self.vehicle_number = None
            self.model = None

        self.courier_id = courier_id


class Client(Person):
    def __init__(self, client_id: int, firstname: str, lastname: str, phone_num: str):
        super().__init__(firstname, lastname, phone_num)
        self.balance = 0.0
        self.__client_id = client_id

    def get_client_id(self) -> int:
        return self.__client_id

    def add_to_balance(self, amount: float):
        if amount > 0:
            self.balance += amount
            print(f"Баланс клієнта {self.firstname} поповнено. Новий баланс: {self.balance}")
        else:
            print("Сума має бути позитивною.")

    @staticmethod
    def is_valid_id(client_id: int) -> bool:
        return client_id > 99

    def getfullname(self) -> str:
        return f"[Клієнт] {self.firstname} {self.lastname}"


def main():
    client1 = Client(client_id=101, firstname="Іван", lastname="Петренко", phone_num="0501112233")

    courier1 = Courier(courier_id=1, first_name="Василь", last_name="Сидоренко", phone_num="0974445566",
                       vehicle_number="BC1234AB", model="Renault Kangoo")
    courier2 = Courier(courier_id=2, first_name="Марія", last_name="Іваненко", phone_num="0637778899")



    print(f"Баланс клієнта {client1.firstname} ДО поповнення: {client1.balance}")
    client1.add_to_balance(500.50)
    print(f"Баланс клієнта {client1.firstname} ПІСЛЯ поповнення: {client1.balance}")

    print(f"Транспорт кур'єра {courier1.firstname}: {courier1.model} (н/з: {courier1.vehicle_num})")
    print(f"Старий номер кур'єра: {courier1.getphone_num()}")
    courier1.upd_phone_num("0970001122")
    print(f"Новий номер кур'єра: {courier1.getphone_num()}")

    print(f"Чи є ID 101 валідним? {Client.is_valid_id(101)}")
    print(f"Чи є ID 50 валідним? {Client.is_valid_id(50)}")

    persons_list = [client1, courier1, courier2]

    print("Виклик методу getfullname() для різних об'єктів:")
    for person in persons_list:
        print(person.getfullname())


    def create_delivery(client: Client, courier: Courier, order_cost: float):
        print(f"\nСпроба створити доставку для {client.getfullname()}")
        if client.balance >= order_cost:
            print(f"Коштів достатньо. Списуємо {order_cost} грн.")
            client.balance -= order_cost
            print(f"Новий баланс: {client.balance} грн.")
            print(f"Замовлення призначено на кур'єра: {courier.getfullname()}")
            if courier.vehicle_num:
                print(f"Доставка буде здійснена на авто: {courier.model}")
            else:
                print("Доставка буде здійснена пішки.")
        else:
            print(f"Доставка неможлива! Недостатньо коштів (потрібно {order_cost}, є {client.balance})")

    create_delivery(client1, courier1, 150.0)
    create_delivery(client1, courier2, 1000.0)


if __name__ == "__main__":
    main()