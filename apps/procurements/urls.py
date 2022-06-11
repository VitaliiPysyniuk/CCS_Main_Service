from django.urls import path

from .views import ProcurementDocumentListCreateView, ProcurementDocumentRetrieveUpdateDestroyView, \
    ProcurementDocumentItemView

urlpatterns = [
    path('', ProcurementDocumentListCreateView.as_view()),
    path('/<int:procurement_id>', ProcurementDocumentRetrieveUpdateDestroyView.as_view()),
    path('/<int:procurement_id>/items', ProcurementDocumentItemView.as_view())
]
