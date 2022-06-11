from django.urls import path, include

urlpatterns = [
    path('/counterparties', include('apps.counterparties.urls'), name='counterparties_app'),
    path('/movements', include('apps.movements.urls'), name='movements_app'),
    path('/orders', include('apps.orders.urls'), name='orders_app'),
    path('/procurements', include('apps.procurements.urls'), name='procurements_app'),
    path('/tmvs', include('apps.tmvs.urls'), name='tmvs_app'),
    path('/warehouses', include('apps.warehouses.urls'), name='warehouses_app')
]
