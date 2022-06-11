from django.urls import path

from .views import MovementDocumentListCreateView, MovementDocumentRetrieveUpdateDestroyView, MovementDocumentItemView

urlpatterns = [
    path('', MovementDocumentListCreateView.as_view()),
    path('/<int:movement_id>', MovementDocumentRetrieveUpdateDestroyView.as_view()),
    path('/<int:movement_id>/items', MovementDocumentItemView.as_view())
]
