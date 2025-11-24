from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('add/', CustomerCreateView.as_view(), name='customer_add'),
    path('<int:customer_id>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('<int:customer_id>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
]
