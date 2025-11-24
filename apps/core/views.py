from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.customers.models import Customer
from apps.inventory.models import Item
from apps.invoices.models import Invoice
from apps.payments.models import Payment


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Date ranges
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        
        # Customer Statistics
        context['total_customers'] = Customer.objects.filter(user=user).count()
        context['active_customers'] = Customer.objects.filter(user=user, status=True).count()
        
        # Inventory Statistics
        context['total_items'] = Item.objects.filter(user=user).count()
        context['low_stock_items'] = Item.objects.filter(user=user, available_qty__lt=10).count()
        
        # Invoice Statistics
        context['total_invoices'] = Invoice.objects.filter(user=user).count()
        context['pending_invoices'] = Invoice.objects.filter(user=user, status='pending').count()
        context['paid_invoices'] = Invoice.objects.filter(user=user, status='paid').count()
        context['draft_invoices'] = Invoice.objects.filter(user=user, status='draft').count()
        
        # Revenue Statistics
        context['total_revenue'] = Invoice.objects.filter(
            user=user, status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        context['this_month_revenue'] = Invoice.objects.filter(
            user=user, status='paid', issue_date__gte=this_month_start
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        context['last_month_revenue'] = Invoice.objects.filter(
            user=user, status='paid', 
            issue_date__gte=last_month_start,
            issue_date__lt=this_month_start
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Payment Statistics
        context['total_payments'] = Payment.objects.filter(user=user).count()
        context['this_month_payments'] = Payment.objects.filter(
            user=user, payment_date__gte=this_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent Activity
        context['recent_invoices'] = Invoice.objects.filter(user=user).select_related('customer').order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.filter(user=user).select_related('invoice__customer').order_by('-payment_date')[:5]
        context['low_stock_list'] = Item.objects.filter(user=user, available_qty__lt=10).order_by('available_qty')[:5]
        
        return context
