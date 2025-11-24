from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from .models import Payment
from .forms import PaymentForm
from apps.invoices.models import Invoice

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user).select_related('invoice', 'invoice__customer')
        
        # Get filter parameters
        method = self.request.GET.get('method')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        search = self.request.GET.get('search')
        
        # Apply filters
        if method:
            queryset = queryset.filter(method=method)
        
        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)
        
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(invoice__invoice_number__icontains=search) |
                Q(transaction_id__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = Payment.METHOD_CHOICES
        context['total_payments'] = self.get_queryset().count()
        return context

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'
    success_url = reverse_lazy('payment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            
            # Update invoice status if fully paid
            invoice = self.object.invoice
            total_paid = sum(p.amount for p in invoice.payments.all())
            
            if total_paid >= invoice.total_amount:
                invoice.status = 'paid'
            elif total_paid > 0:
                invoice.status = 'pending'
            
            invoice.save()
            
        return super().form_valid(form)

class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'
    pk_url_kwarg = 'payment_id'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
