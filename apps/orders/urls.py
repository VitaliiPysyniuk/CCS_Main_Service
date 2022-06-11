from django.urls import path

from .views import OrderDocumentListCreateView, OrderDocumentRetrieveUpdateDestroyView, OrderDocumentItemView

urlpatterns = [
    path('', OrderDocumentListCreateView.as_view()),
    path('/<int:order_id>', OrderDocumentRetrieveUpdateDestroyView.as_view()),
    path('/<int:order_id>/items', OrderDocumentItemView.as_view())
]
