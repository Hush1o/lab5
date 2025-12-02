from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainapp.views import ClientViewSet, OfficeViewSet, ShipmentViewSet, shipment_report

router = DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('offices', OfficeViewSet, basename='offices')
router.register('shipments', ShipmentViewSet, basename='shipments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/report/', shipment_report),
    path('api/', include(router.urls)),
    path('', include('web.urls')),
]
