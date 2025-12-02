from django.db import models


class Clients(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Offices(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = 'Offices'

    def __str__(self):
        return f"{self.city}, {self.address}"


class Shipments(models.Model):

    client = models.ForeignKey('Clients', on_delete=models.CASCADE, db_column='client_id')

    from_office = models.ForeignKey('Offices', on_delete=models.CASCADE, db_column='from_office_id',
                                    related_name='from_shipments')
    to_office = models.ForeignKey('Offices', on_delete=models.CASCADE, db_column='to_office_id',
                                  related_name='to_shipments')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')


    when_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Shipments'

    def __str__(self):
        return f"Shipment #{self.id} (from {self.from_office.city} to {self.to_office.city})"


class Packages(models.Model):
    shipment = models.ForeignKey('Shipments', on_delete=models.CASCADE, db_column='shipment_id')
    description = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Packages'


class Payments(models.Model):
    shipment = models.ForeignKey('Shipments', on_delete=models.CASCADE, db_column='shipment_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Payments'


class Couriers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    vehicle_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'Couriers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tracking(models.Model):
    shipment = models.ForeignKey('Shipments', on_delete=models.CASCADE, db_column='shipment_id')
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tracking'


class Delivery(models.Model):
    shipment = models.OneToOneField('Shipments', on_delete=models.CASCADE, db_column='shipment_id')

    courier = models.ForeignKey('Couriers', on_delete=models.SET_NULL, null=True, blank=True, db_column='courier_id')
    delivery_address = models.CharField(max_length=255)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Scheduled')

    class Meta:
        db_table = 'Delivery'