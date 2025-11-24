from django.urls import path
from .views import PaymentListView, PaymentCreateView, PaymentDetailView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment_list'),
    path('add/', PaymentCreateView.as_view(), name='payment_add'),
    path('<int:payment_id>/', PaymentDetailView.as_view(), name='payment_detail'),
]
