# mainapp/repository.py
from abc import abstractmethod, ABC
from django.db.models import Count, Avg, Sum
from django.utils import timezone

from .models import Clients, Shipments, Offices

class BaseRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def update(self, id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

class DjangoBaseRepository(BaseRepository):
    def __init__(self, model_class):
        self.model = model_class

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id: int):
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def create(self, data: dict):
        return self.model.objects.create(**data)

    def update(self, id: int, data: dict):
        obj = self.get_by_id(id)
        if not obj:
            return None
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    def delete(self, id: int):
        obj = self.get_by_id(id)
        if not obj:
            return False
        obj.delete()
        return True

class ClientRepository(DjangoBaseRepository):
    def __init__(self):
        super().__init__(Clients)

class ShipmentRepository(DjangoBaseRepository):
    def __init__(self):
        super().__init__(Shipments)

    # додаткові репорт-методи
    def shipments_summary(self):
        total = Shipments.objects.count()
        by_status_qs = Shipments.objects.values('status').annotate(count=Count('id'))
        by_status = {row['status']: row['count'] for row in by_status_qs}
        avg_price = Shipments.objects.aggregate(avg_price=Avg('price'))['avg_price'] or 0
        # shipments per city (by from_office city)
        per_city_qs = Shipments.objects.select_related('from_office').values('from_office__city').annotate(count=Count('id'))
        per_city = {row['from_office__city'] or 'Unknown': row['count'] for row in per_city_qs}
        return {
            'total_shipments': total,
            'shipments_by_status': by_status,
            'average_price': float(avg_price),
            'shipments_by_from_city': per_city,
        }

class OfficeRepository(DjangoBaseRepository):
    def __init__(self):
        super().__init__(Offices)
