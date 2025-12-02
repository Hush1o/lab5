from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .repositories import ClientRepository, OfficeRepository, ShipmentRepository
from .serializers import ClientSerializer, OfficeSerializer, ShipmentSerializer

from django.db.models import Count, Sum
from .models import Shipments


class ClientViewSet(viewsets.ViewSet):
    repo = ClientRepository()

    def list(self, request):
        clients = self.repo.get_all()
        return Response(ClientSerializer(clients, many=True).data)

    def retrieve(self, request, pk=None):
        client = self.repo.get_by_id(pk)
        if not client:
            return Response({"error": "Client not found"}, status=404)
        return Response(ClientSerializer(client).data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            obj = self.repo.create(serializer.validated_data)
            return Response(ClientSerializer(obj).data, status=201)
        return Response(serializer.errors, status=400)


class OfficeViewSet(viewsets.ViewSet):
    repo = OfficeRepository()

    def list(self, request):
        offices = self.repo.get_all()
        return Response(OfficeSerializer(offices, many=True).data)

    def retrieve(self, request, pk=None):
        office = self.repo.get_by_id(pk)
        if not office:
            return Response({"error": "Office not found"}, status=404)
        return Response(OfficeSerializer(office).data)

    def create(self, request):
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            obj = self.repo.create(serializer.validated_data)
            return Response(OfficeSerializer(obj).data, status=201)
        return Response(serializer.errors, status=400)


class ShipmentViewSet(viewsets.ViewSet):
    repo = ShipmentRepository()

    def list(self, request):
        shipments = self.repo.get_all()
        return Response(ShipmentSerializer(shipments, many=True).data)

    def retrieve(self, request, pk=None):
        shipment = self.repo.get_by_id(pk)
        if not shipment:
            return Response({"error": "Shipment not found"}, status=404)
        return Response(ShipmentSerializer(shipment).data)

    def create(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            obj = self.repo.create(serializer.validated_data)
            return Response(ShipmentSerializer(obj).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shipment_report(request):
    data = {
        "total_shipments": Shipments.objects.count(),
        "shipments_by_status": Shipments.objects.values("status").annotate(count=Count("id")),
        "avg_price": Shipments.objects.all().aggregate(avg=Sum("price"))
    }
    return Response(data)

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def shipment_report(request):
    return Response({
        "total_shipments": 0,
        "message": "Report generated successfully"
    })
