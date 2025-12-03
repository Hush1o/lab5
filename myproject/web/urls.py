from django.urls import path
from . import views

urlpatterns = [
    # Clients
    path("", views.clients_list, name="home"),
    path("clients/", views.clients_list, name="clients_list"),
    path("clients/<int:id>/", views.client_detail, name="client_detail"),
    path("clients/<int:id>/delete/", views.client_delete, name="client_delete"),
    path("clients/create/", views.client_form, name="client_create"),

    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),

    # Offices
    path('offices/', views.offices_list, name="offices_list"),
    path('offices/add/', views.office_create, name="office_create"),
    path('offices/<int:pk>/', views.office_detail, name="office_detail"),
    path('offices/<int:pk>/edit/', views.office_edit, name="office_edit"),
    path('offices/<int:pk>/delete/', views.office_delete, name="office_delete"),

    # Shipments
    path('shipments/', views.shipments_list, name="shipments_list"),
    path('shipments/add/', views.shipment_create, name="shipment_create"),
    path('shipments/<int:pk>/', views.shipment_detail, name="shipment_detail"),
    path('shipments/<int:pk>/edit/', views.shipment_edit, name="shipment_edit"),
    path('shipments/<int:pk>/delete/', views.shipment_delete, name="shipment_delete"),

    path("api/clients/", views.api_clients_list, name="api_clients_list"),
    path("api/clients/<int:id>/", views.api_client_detail, name="api_client_detail"),

# OFFICES
    path("offices/", views.offices_list, name="offices_list"),
    path("offices/<int:pk>/", views.office_detail, name="office_detail"),
    path("offices/create/", views.office_create, name="office_create"),
    path("offices/<int:pk>/edit/", views.office_edit, name="office_edit"),
    path("offices/<int:pk>/delete/", views.office_delete, name="office_delete"),

# SHIPMENTS
    path("shipments/", views.shipments_list, name="shipments_list"),
    path("shipments/<int:pk>/", views.shipment_detail, name="shipment_detail"),
    path("shipments/create/", views.shipment_create, name="shipment_create"),
    path("shipments/<int:pk>/edit/", views.shipment_edit, name="shipment_edit"),
    path("shipments/<int:pk>/delete/", views.shipment_delete, name="shipment_delete"),

]
