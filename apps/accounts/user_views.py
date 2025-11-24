from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Users, User_Roles
from .user_forms import UserManagementForm, UserFilterForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require Admin role"""
    def test_func(self):
        return (self.request.user.is_authenticated and 
                self.request.user.role is not None and
                self.request.user.role.role_name == 'Admin')
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('dashboard')


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """List all users with filtering and search"""
    model = Users
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Users.objects.select_related('role').all()
        
        # Get filter parameters
        role_id = self.request.GET.get('role')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        # Apply filters
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        if status == '1':
            queryset = queryset.filter(status=True)
        elif status == '0':
            queryset = queryset.filter(status=False)
        
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = UserFilterForm(self.request.GET)
        context['total_users'] = self.get_queryset().count()
        return context


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Create new user"""
    model = Users
    form_class = UserManagementForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = False
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.email} created successfully!')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Edit existing user"""
    model = Users
    form_class = UserManagementForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    pk_url_kwarg = 'user_id'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = True
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.email} updated successfully!')
        return super().form_valid(form)


class UserToggleStatusView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Toggle user active/inactive status"""
    def post(self, request, user_id):
        user = get_object_or_404(Users, pk=user_id)
        
        # Prevent admin from deactivating themselves
        if user.pk == request.user.pk:
            messages.error(request, 'You cannot deactivate your own account.')
            return redirect('user_list')
        
        # Toggle status
        user.status = not user.status
        user.save()
        
        status_text = 'activated' if user.status else 'deactivated'
        messages.success(request, f'User {user.email} has been {status_text}.')
        
        return redirect('user_list')


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Delete user with confirmation"""
    model = Users
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    pk_url_kwarg = 'user_id'
    
    def dispatch(self, request, *args, **kwargs):
        """Prevent admin from deleting themselves"""
        user = self.get_object()
        if user.pk == request.user.pk:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f'User {user.email} has been deleted.')
        return super().delete(request, *args, **kwargs)
