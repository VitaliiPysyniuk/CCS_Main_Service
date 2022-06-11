from django.urls import path

from .views import TMVTypeListCreateView, TMVTypeRetrieveUpdateDestroyView, TMVUnitListCreateView, \
    TMVUnitRetrieveUpdateDestroyView, TMVListCreateView, TMVRetrieveUpdateDestroyView, TMVWarehouseListCreateView, \
    TMVWarehouseRetrieveUpdateDestroyView

urlpatterns = [
    path('', TMVListCreateView.as_view()),
    path('/<int:tmv_id>', TMVRetrieveUpdateDestroyView.as_view()),
    path('/units/<int:unit_id>', TMVUnitRetrieveUpdateDestroyView.as_view()),
    path('/types', TMVTypeListCreateView.as_view()),
    path('/types/<int:type_id>', TMVTypeRetrieveUpdateDestroyView.as_view()),
    path('/units', TMVUnitListCreateView.as_view()),
    path('/units/<int:unit_id>', TMVUnitRetrieveUpdateDestroyView.as_view()),
    path('/tmvs_warehouses', TMVWarehouseListCreateView.as_view()),
    path('/tmvs_warehouses/<int:item_id>', TMVWarehouseRetrieveUpdateDestroyView.as_view()),
]
