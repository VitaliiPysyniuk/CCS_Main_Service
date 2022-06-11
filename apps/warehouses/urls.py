from django.urls import path

from .views import WarehouseListCreateView, WarehouseRetrieveUpdateDestroyView, WarehouseItemView, WarehouseItemsView, \
    WarehouseTMVTurnoverView

urlpatterns = [
    path('', WarehouseListCreateView.as_view()),
    path('/<int:warehouse_id>', WarehouseRetrieveUpdateDestroyView.as_view()),
    path('/<int:warehouse_id>/items', WarehouseItemsView.as_view()),
    path('/<int:warehouse_id>/items/<int:tmv_id>', WarehouseItemView.as_view()),
    path('/<int:warehouse_id>/turnover', WarehouseTMVTurnoverView.as_view()),
]
