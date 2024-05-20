# workerdata/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkerViewSet, ReceiptViewSet, AddWorkerView

router = DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_worker/', AddWorkerView.as_view(), name='add_worker'),
]
