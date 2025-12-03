from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import Clients, Offices, Shipments
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from mainapp.models import Clients

class ClientForm(ModelForm):
    class Meta:
        model = Clients
        fields = ["first_name", "last_name", "phone"]

def client_form(request, id=None):
    if id:
        client = Clients.objects.get(id=id)
    else:
        client = None

    form = ClientForm(request.POST or None, instance=client)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("clients_list")

    return render(request, "web/client_form.html", {"form": form})


def clients_list(request):
    clients = Clients.objects.all()
    return render(request, "web/clients_list.html", {"clients": clients})

def client_detail(request, pk):
    client = get_object_or_404(Clients, id=pk)
    return render(request, "web/client_detail.html", {"client": client})

def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("clients_list")
    return render(request, "web/client_form.html", {"form": form, "title": "Add client"})

def client_edit(request, pk):
    client = get_object_or_404(Clients, id=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect("client_detail", pk=pk)
    return render(request, "web/client_form.html", {"form": form, "title": "Edit client"})

def client_delete(request, pk):
    client = get_object_or_404(Clients, id=pk)
    if request.method == "POST":
        client.delete()
        return redirect("clients_list")
    return render(request, "web/client_delete.html", {"client": client})


# -------- OFFICES --------
class OfficeForm(ModelForm):
    class Meta:
        model = Offices
        fields = ["city", "address"]

def offices_list(request):
    offices = Offices.objects.all()
    return render(request, "web/offices_list.html", {"offices": offices})

def office_detail(request, pk):
    office = get_object_or_404(Offices, id=pk)
    return render(request, "web/office_detail.html", {"office": office})

def office_create(request):
    form = OfficeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("offices_list")
    return render(request, "web/office_form.html", {"form": form})

def office_edit(request, pk):
    office = get_object_or_404(Offices, id=pk)
    form = OfficeForm(request.POST or None, instance=office)
    if form.is_valid():
        form.save()
        return redirect("office_detail", pk=pk)
    return render(request, "web/office_form.html", {"form": form})

def office_delete(request, pk):
    office = get_object_or_404(Offices, id=pk)
    if request.method == "POST":
        office.delete()
        return redirect("offices_list")
    return render(request, "web/office_delete.html", {"office": office})


# -------- SHIPMENTS --------
class ShipmentForm(ModelForm):
    class Meta:
        model = Shipments
        fields = ["client", "from_office", "to_office", "price", "status"]

def shipments_list(request):
    shipments = Shipments.objects.all()
    return render(request, "web/shipments_list.html", {"shipments": shipments})

def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)
    return render(request, "web/shipment_detail.html", {"shipment": shipment})

def shipment_create(request):
    form = ShipmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("shipments_list")
    return render(request, "web/shipment_form.html", {"form": form})

def shipment_edit(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)
    form = ShipmentForm(request.POST or None, instance=shipment)
    if form.is_valid():
        form.save()
        return redirect("shipment_detail", pk=pk)
    return render(request, "web/shipment_form.html", {"form": form})

def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)
    if request.method == "POST":
        shipment.delete()
        return redirect("shipments_list")
    return render(request, "web/shipment_delete.html", {"shipment": shipment})


@csrf_exempt
def api_clients_list(request):
    """
    GET  /api/clients/  -> список клієнтів (JSON)
    POST /api/clients/  -> створити клієнта
    """
    if request.method == "GET":
        clients = Clients.objects.all()
        data = [
            {
                "id": c.id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "phone": c.phone,
            }
            for c in clients
        ]
        return JsonResponse(data, safe=False, status=200)

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        first_name = body.get("first_name")
        last_name = body.get("last_name")
        phone = body.get("phone")

        if not first_name or not last_name:
            return JsonResponse({"error": "first_name and last_name are required"}, status=400)

        client = Clients.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        return JsonResponse(
            {
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "phone": client.phone,
            },
            status=201,
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_client_detail(request, id):
    """
    GET    /api/clients/<id>/  -> один клієнт
    PUT    /api/clients/<id>/  -> оновити
    DELETE /api/clients/<id>/  -> видалити
    """
    try:
        client = Clients.objects.get(id=id)
    except Clients.DoesNotExist:
        return JsonResponse({"error": "Client not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(
            {
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "phone": client.phone,
            },
            status=200,
        )

    if request.method == "PUT":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        client.first_name = body.get("first_name", client.first_name)
        client.last_name = body.get("last_name", client.last_name)
        client.phone = body.get("phone", client.phone)
        client.save()

        return JsonResponse(
            {
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "phone": client.phone,
            },
            status=200,
        )

    if request.method == "DELETE":
        client.delete()
        return JsonResponse({}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# -------- OFFICES --------

def offices_list(request):
    offices = Offices.objects.all()
    return render(request, "web/offices_list.html", {"offices": offices})


def office_detail(request, pk):
    office = get_object_or_404(Offices, id=pk)
    return render(request, "web/office_detail.html", {"office": office})


def office_create(request):
    if request.method == "POST":
        city = request.POST.get("city")
        address = request.POST.get("address")
        Offices.objects.create(city=city, address=address)
        return redirect("offices_list")
    return render(request, "web/office_form.html")


def office_edit(request, pk):
    office = get_object_or_404(Offices, id=pk)

    if request.method == "POST":
        office.city = request.POST.get("city")
        office.address = request.POST.get("address")
        office.save()
        return redirect("office_detail", pk=pk)

    return render(request, "web/office_form.html", {"office": office})


def office_delete(request, pk):
    office = get_object_or_404(Offices, id=pk)
    if request.method == "POST":
        office.delete()
        return redirect("offices_list")
    return render(request, "web/office_delete.html", {"office": office})
# -------- SHIPMENTS --------

def shipments_list(request):
    shipments = Shipments.objects.all()
    return render(request, "web/shipments_list.html", {"shipments": shipments})


def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)
    return render(request, "web/shipment_detail.html", {"shipment": shipment})


def shipment_create(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        from_office_id = request.POST.get("from_office")
        to_office_id = request.POST.get("to_office")
        price = request.POST.get("price")
        status = request.POST.get("status")

        Shipments.objects.create(
            client_id=client_id,
            from_office_id=from_office_id,
            to_office_id=to_office_id,
            price=price,
            status=status,
        )
        return redirect("shipments_list")

    return render(request, "web/shipment_form.html")


def shipment_edit(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)

    if request.method == "POST":
        shipment.client_id = request.POST.get("client")
        shipment.from_office_id = request.POST.get("from_office")
        shipment.to_office_id = request.POST.get("to_office")
        shipment.price = request.POST.get("price")
        shipment.status = request.POST.get("status")
        shipment.save()
        return redirect("shipment_detail", pk=pk)

    return render(request, "web/shipment_form.html", {"shipment": shipment})


def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipments, id=pk)
    if request.method == "POST":
        shipment.delete()
        return redirect("shipments_list")
    return render(request, "web/shipment_delete.html", {"shipment": shipment})

class ClientUpdateView(UpdateView):
    model = Clients
    fields = ['first_name', 'last_name', 'phone', 'email'] # Поля, які можна редагувати
    template_name = 'web/client_form.html'
    success_url = reverse_lazy('clients_list')