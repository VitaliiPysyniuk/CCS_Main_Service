from django.urls import path

from .views import CounterpartyTypeListCreateView, CounterpartyTypeRetrieveUpdateDestroyView, \
    CounterpartyListCreateView, CounterpartyRetrieveUpdateDestroyView, CounterpartyFilterRetrieveView

urlpatterns = [
    path('', CounterpartyListCreateView.as_view(), name='get_all_create_counterparties'),
    path('/<int:counterparty_id>', CounterpartyRetrieveUpdateDestroyView.as_view(),
         name='get_update_delete_counterparty_by_id'),
    path('/info', CounterpartyFilterRetrieveView.as_view(), name='get_single_counterparty_with_queryparams'),
    path('/types', CounterpartyTypeListCreateView.as_view(), name='get_all_create_counterparty_types'),
    path('/types/<int:type_id>', CounterpartyTypeRetrieveUpdateDestroyView.as_view(),
         name='get_update_delete_counterparty_type_by_id')
]
