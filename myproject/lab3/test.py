from mainapp.repositories import ClientRepository, ShipmentRepository, OfficeRepository

client_repo = ClientRepository()
shipment_repo = ShipmentRepository()
office_repo = OfficeRepository()


print("\n1. Демонстрація для 'Клієнтів'")

print("Створюю нового клієнта 'Іван Петренко'...")
new_client_data = {
    'first_name': 'Іван',
    'last_name': 'Петренко',
    'email': 'ivan@example.com',
    'phone': '+380501234567'
}
created_client = client_repo.create(new_client_data)
print(f"Створено клієнта: {created_client}")


print("\nОтримую всіх клієнтів...")
all_clients = client_repo.get_all()
print(f"Знайдено {all_clients.count()} клієнтів:")
for client in all_clients:
    print(f"  ID: {client.id}, Ім'я: {client.first_name} {client.last_name}")


print(f"\nШукаю клієнта по ID: {created_client.id}...")
found_client = client_repo.get_by_id(created_client.id)
print(f"Знайдено: {found_client}")



print("\n2. Демонстрація для 'Відділень'")

print("Отримую всі відділення...")
all_offices = office_repo.get_all()
print(f"Знайдено {all_offices.count()} відділень:")
for office in all_offices:
    print(f"  ID: {office.id}, Адреса: {office.address}")


print("\n3. Демонстрація для 'Відправлень'")

print("Отримую всі відправлення...")
all_shipments = shipment_repo.get_all()
print(f"Знайдено {all_shipments.count()} відправлень:")
for shipment in all_shipments:
    print(f"  ID: {shipment.id}, Статус: {shipment.status}")

print("Демонстрацію завершено.")

exit()

from mainapp.models import Clients

try:
    client_to_delete = Clients.objects.get(email='ivan@example.com')

    client_to_delete.delete()

    print(f"[OK] Клієнта 'ivan@example.com' було успішно видалено.")

except Clients.DoesNotExist:
    print("[INFO] Клієнта 'ivan@example.com' не знайдено. База даних вже чиста.")

