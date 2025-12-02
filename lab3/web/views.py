from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import Clients, Offices, Shipments
from django.forms import ModelForm

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
