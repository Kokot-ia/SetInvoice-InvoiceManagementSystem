from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Customer
from .forms import CustomerForm

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

    def get_queryset(self):
        queryset = Customer.objects.filter(user=self.request.user).select_related('user')
        
        # Get filter parameters
        status = self.request.GET.get('status')
        city = self.request.GET.get('city')
        search = self.request.GET.get('search')
        
        # Apply filters
        if status == 'active':
            queryset = queryset.filter(status=True)
        elif status == 'inactive':
            queryset = queryset.filter(status=False)
        
        if city:
            queryset = queryset.filter(city__iexact=city)
        
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(customer_name__icontains=search) |
                Q(email__icontains=search) |
                Q(contact_no__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique cities for filter dropdown
        context['cities'] = Customer.objects.filter(
            user=self.request.user
        ).values_list('city', flat=True).distinct().order_by('city')
        context['total_customers'] = self.get_queryset().count()
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')
    pk_url_kwarg = 'customer_id'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')
    pk_url_kwarg = 'customer_id'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
