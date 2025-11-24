from django.urls import path
from .views import (
    InvoiceListView, InvoiceCreateView, InvoiceUpdateView, 
    InvoiceDetailView, InvoicePDFView
)

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('add/', InvoiceCreateView.as_view(), name='invoice_add'),
    path('<int:invoice_id>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('<int:invoice_id>/edit/', InvoiceUpdateView.as_view(), name='invoice_edit'),
    path('<int:invoice_id>/pdf/', InvoicePDFView.as_view(), name='invoice_pdf'),
]
